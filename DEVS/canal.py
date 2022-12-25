from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass

KNOT = 1.852  # 1 knot (1 nautical mile per hour) is 1.852 km/h

@dataclass(repr=False)
class CanalState:
	## The length of the canal
	length: float
	vessels: list

	def __repr__(self):
		return f"CanalState(length={self.length}, vessels={[t for v,t in self.vessels]})"

class Canal(AtomicDEVS):
	"""
	Special kind of Waterway. Identifies a section of the port over which Vessels sail in both directions. Vessels are
	limited to their average velocity and they are not allowed to pass each other. This implies: if there is a Vessel A
	at velocity v in front of another Vessel B, with desired velocity w, B's velocity becomes min(w, v). Just like
	Waterways, Canals also have a distance, which can be used to obtain the time spent on this Canal.
	"""
	def __init__(self, name: str, length: float):
		super(Canal, self).__init__(name)

		# Add the output and input ports
		self.ship_in = self.addInPort("ship_in")
		self.ship_out = self.addOutPort("ship_out")

		# Initialize the internal state
		self.state = CanalState(length, [])

	def extTransition(self, inputs):
		# Update the times
		self.state.vessels = [(v,t-self.elapsed) for v,t in self.state.vessels]

		if self.ship_in in inputs:
			vessel =  inputs[self.ship_in]
			# Make the avg speed the average of the vessel in the canal, if there are none infinity
			avg_speed = min([v.avg_velocity for v,t in self.state.vessels]) if len(self.state.vessels) else INFINITY
			avg_speed = min(vessel.avg_velocity, avg_speed)
			# Knots -> KM/H -> M/H -> M/m
			speed = avg_speed*KNOT*1000/60  # in M/m
			time = self.state.length / speed # : M/(M/m) -> m
			self.state.vessels.append((vessel, time))

		return self.state

	def intTransition(self):
		# Update the times
		self.state.vessels = [(v, t - self.timeAdvance()) for v, t in self.state.vessels]
		# Find the entry that is 0
		index = self.state.vessels.index(next((v,t) for v,t in self.state.vessels if t == 0))
		# Remove that entry
		del  self.state.vessels[index]
		return self.state

	def outputFnc(self):
		# Return the first ready vessel
		# NOTE: Since this is before the intTransition the time is not yet updated
		return {self.ship_out: next((v for v,t in self.state.vessels if t == self.timeAdvance())) }

	def timeAdvance(self):
		if len(self.state.vessels) == 0:  # If there are no vessels
			return INFINITY

		# Return the smallest departure time
		departure_times = [t for _,t in self.state.vessels]
		return min(departure_times)

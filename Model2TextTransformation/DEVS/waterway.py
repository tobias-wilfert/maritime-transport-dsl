from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass

KNOT = 1.852  # 1 knot (1 nautical mile per hour) is 1.852 km/h

@dataclass(repr=False)
class WaterwayState:
	## The length of the waterway
	length: float
	## List of tuples (Vessel, departure_time)
	vessels: list

	def __repr__(self):
		return f"WaterwayState(length={self.length}, vessels={[t for v,t in self.vessels]})"

class Waterway(AtomicDEVS):
	"""
	Identifies a section of the river over which Vessels sail in one directions. There is no maximal speed limit on
	this segment and vessels are allowed to pass each other. Waterways have a distance (see the map above), which, when
	combined with a Vessel's velocity, allows identification of the time spent on this Waterway. For simplicity reasons,
	there is no capacity on a Waterway.
	"""
	def __init__(self, name: str, length: float):
		super(Waterway, self).__init__(name)

		# Add the output and input ports
		self.ship_in = self.addInPort("ship_in")
		self.ship_out = self.addOutPort("ship_out")

		# Initialize the internal state
		self.state = WaterwayState(length, [])

	def extTransition(self, inputs):
		# Update the times
		self.state.vessels = [(v,t-self.elapsed) for v,t in self.state.vessels]

		if self.ship_in in inputs:
			vessel =  inputs[self.ship_in]
			# Knots -> KM/H -> M/H -> M/m
			speed = vessel.max_velocity*KNOT*1000/60  # in M/m
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

import numpy
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass
# Out include
from events import PortDepartureRequest

@dataclass(repr=False)
class DockState:
	## The id of the Dock (needed for sending messages to the control tower)
	quay_id: int
	## List of tuples (Vessel, departure_time)
	vessels: list

	def __repr__(self):
		return f"DockState(vessels={self.vessels})"


class Dock(AtomicDEVS):
	"""
	Identifies a quay or wharf with multiple mooring possibilities. Each Dock is able to hold 50 Vessels and is
	identified by a unique quay number (see map), such that Vessels know which way to go in Confluences.
	When a Vessel arrives, the Dock samples from a normal distribution with average 36 hours and standard deviation 12
	hours. This sample identifies how long a Vessel needs to stay at a Dock. A Vessel remains at least 6 hours at the
	port. After this sampled time period has ended, the Dock sends a PortDepartureRequest to the ControlTower,
	releasing its position at the Dock before sailing to the Sea.
	"""
	def __init__(self, quay_id: int, seed = 0, vessels=None, avg_time=36*60, sd_time=12*60):
		super(Dock, self).__init__(f"Dock#{quay_id}")

		# Add the output and input ports
		self.ship_in = self.addInPort("ship_in")
		self.ship_out = self.addOutPort("ship_out")
		self.message_out = self.addOutPort("message_out")

		## Generate local instances of the random classes so that we avoid a global state
		self.random_numpy_state = numpy.random.RandomState(seed)
		self.avg_time = avg_time
		self.sd_time = sd_time

		# Initialize the internal state
		if vessels is None:
			vessels = []
		self.state = DockState(quay_id, vessels)

	def extTransition(self, inputs):
		# Update the times
		self.state.vessels = [(v,t-self.elapsed) for v,t in self.state.vessels]

		if self.ship_in in inputs:
			# Calculate how long the ship needs to wait at the dock
			vessel =  inputs[self.ship_in]
			time = self.random_numpy_state.normal(self.avg_time, self.sd_time)
			# time = 10 # TODO: Fix the time spend in the port for debugging
			# Update the destination of the vessel
			vessel.destination = 0
			self.state.vessels.append((vessel, time))

		return self.state

	def intTransition(self):
		# Update the times
		self.state.vessels = [(v, t - self.timeAdvance()) for v, t in self.state.vessels]
		# Find the entry that is 0
		index = self.state.vessels.index(next((v, t) for v, t in self.state.vessels if t == 0))
		# Remove that entry
		del self.state.vessels[index]
		return self.state

	def outputFnc(self):
		# Return the first ready vessel and also send a message to the control tower
		# NOTE: Since this is before the intTransition the time is not yet updated
		vessel = next((v for v,t in self.state.vessels if t == self.timeAdvance()))
		return {self.ship_out: vessel,
				self.message_out: PortDepartureRequest(vessel.unique_id, self.state.quay_id) }

	def timeAdvance(self):
		if len(self.state.vessels) == 0:  # If there are no vessels
			return INFINITY

		# Return the smallest departure time
		departure_times = [t for _, t in self.state.vessels]
		return min(departure_times)

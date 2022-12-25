from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass
# Our includes:
from events import PortEntryRequest, Vessel


@dataclass(repr=False)
class AnchorpointState:
	""" The state of the Anchorpoint"""
	## The simulation time inorder to know how long a vessel has waited
	t_sim = 0.0
	## The label of the stat either: idle, sending
	label = "idle"
	## All the vessels that are currently in the Anchorpoint indexed by their unique_id
	vessels = {}
	## The arrival time of the vessels
	vessel_arrival = {}
	## The departure time of the vessels
	vessel_departure = {}
	## All the messages that need to be sent since multiple can arrive at the same time
	message_queue = []
	## The message that is currently being sent
	processing = None
	## All the vessels that have departed that have departed the anchor state
	departed_vessels = []

	def __repr__(self):
		return f"AnchorpointState(label='{self.label}', len(message_queue)={len(self.message_queue)}, #departed_vessels={len(self.departed_vessels)}, processing={self.processing})"

	def avg_waiting_time(self):
		"""
		@Note: Should only be called after the simulation has concluded as this examines the state
		:return: Returns the average waiting time for a vessel in the Anchorpoint
		"""
		waiting_times = [self.vessel_departure[vessel.unique_id] - self.vessel_arrival[vessel.unique_id] for vessel in
						 self.departed_vessels]
		return sum(waiting_times) / len(waiting_times) if len(waiting_times) else 0

	def time_per_vessel(self):
		"""
		@Note: Should only be called after the simulation has concluded as this examines the state
		Can be used to generate interesting plots like waiting time per vessel and waiting time over time
		:return: Returns a list of tuples (vessel, arrival_time, departure_time)
		"""
		return [(vessel, self.vessel_departure[vessel.unique_id], self.vessel_arrival[vessel.unique_id]) for vessel in
				self.departed_vessels]


class Anchorpoint(AtomicDEVS):
	def __init__(self):
		super(Anchorpoint, self).__init__("Anchorpoint")
		# Add the output and input ports
		self.ship_in = self.addInPort("ship_in")  # input from the Generator
		self.message_in = self.addInPort("message_in")  # input to receive PortEntryPermission from ControlTower
		self.ship_out = self.addOutPort("ship_out")  # output to move the ships to the port.
		self.message_out = self.addOutPort("message_out")  # output to send the PortEntryRequest to the ControlTower

		# Initialize the internal state
		self.state = AnchorpointState()

	def extTransition(self, inputs):
		self.state.t_sim += self.elapsed  # Keep track of the time for the statistics

		# Since both of these can happen at the same time, need to do some magic
		if self.ship_in in inputs:
			ship_id = inputs[self.ship_in].unique_id
			self.state.message_queue.append(PortEntryRequest(ship_id))
			self.state.vessel_arrival[ship_id] = self.state.t_sim
			self.state.vessels[ship_id] = inputs[self.ship_in]

		if self.message_in in inputs:
			ship_id = inputs[self.message_in].ship_id
			vessel = self.state.vessels[ship_id]
			vessel.destination = inputs[self.message_in].quay_id
			self.state.message_queue.append(vessel)

		# Check if we are idle if so switch to sending and send the message
		if not self.state.processing and self.state.message_queue:
			self.state.processing = self.state.message_queue.pop(0)
			self.state.label = "sending"

		return self.state

	def intTransition(self):
		# Note: "This is only called when we are outputting an event" - The Docs
		self.state.t_sim += self.timeAdvance()  # Keep track of the time for the statistics

		if isinstance(self.state.processing, Vessel):  # Collect statistics
			self.state.vessel_departure[self.state.processing.unique_id] = self.state.t_sim
			self.state.departed_vessels.append(self.state.processing)
			# del self.state.vessels[elf.state.processing.unique_id] # TODO: This might cause trouble

		# If there are still messages left to send, send them
		if self.state.message_queue:
			self.state.processing = self.state.message_queue.pop(0)
			self.state.label = "sending"
		else:
			self.state.processing = None
			self.state.label = "idle"

		return self.state

	def outputFnc(self):
		port = self.ship_out if isinstance(self.state.processing, Vessel) else self.message_out
		return {port: self.state.processing}

	def timeAdvance(self):
		return {"idle": INFINITY,
				"sending": 0}[self.state.label]

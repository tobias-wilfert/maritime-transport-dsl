from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass
# Our includes:
from events import PortEntryPermission, PortDepartureRequest


@dataclass(repr=False)
class ControlTowerState:
	"""
	Keeps track of all the available Docks and their capacities. For the sake of simplicity, a Dock is reserved by a
	Vessel, as soon as the ControlTower sends the PortEntryPermission message.
	"""
	## The label of the stat either: idle, sending
	label = "idle"
	## The idle docks, each dock has capacity 50
	idle_docks = sorted([1,2,3,4,5,6,7,8] * 50) # TODO: Changing this already yields some changes
	# idle_docks = sorted([1, 2] * 50) # TODO: Restrict the number of docs for debugging
	## All the PortEntryRequests that have not yet been followed up with a PortEntryPermission
	message_queue = []
	## The message that is currently being sent
	processing = None

	def __repr__(self):
		return f"ControlTowerState(label='{self.label}', #idle_docks={len(self.idle_docks)}, #queued_messages={len(self.message_queue)} processing={self.processing})"


class ControlTower(AtomicDEVS):
	"""
	Communication point for accessing the port. It can communicate with the Anchorpoint to identify which ships are
	allowed to enter and to which quay/Dock they must sail.
	"""

	def __init__(self):
		super(ControlTower, self).__init__("Control Tower")
		# Add the output and input ports
		self.message_in = self.addInPort("message_in")
		self.message_out = self.addOutPort("message_out")

		# Initialize the internal state
		self.state = ControlTowerState()

	def extTransition(self, inputs):
		# Could receive two different messages on the same input
		if not self.message_in in inputs:  # If there is no message skip
			return self.state

		message = inputs[self.message_in]
		if isinstance(message, PortDepartureRequest):  # New dock became free
			self.state.idle_docks.append(message.quay_id)
			if not self.state.processing and self.state.message_queue:
				self.state.processing = self.state.message_queue.pop(0)
				self.state.label = "sending"
		else:  # New PortEntryRequests
			if self.state.idle_docks and not self.state.processing:
				self.state.processing = message.ship_id
				self.state.label = "sending"
			else:
				self.state.message_queue.append(message.ship_id)

		return self.state

	def intTransition(self):
		self.state.idle_docks.pop(0)
		# If there are still messages left to send, send them
		if self.state.message_queue and self.state.idle_docks:
			self.state.processing = self.state.message_queue.pop(0)
			self.state.label = "sending"
		else:
			self.state.processing = None
			self.state.label = "idle"

		return self.state

	def outputFnc(self):
		ship_id = self.state.processing
		destination = self.state.idle_docks[0]
		return {self.message_out: PortEntryPermission(ship_id, destination)}

	def timeAdvance(self):
		return {"idle": INFINITY,
				"sending": 0}[self.state.label]

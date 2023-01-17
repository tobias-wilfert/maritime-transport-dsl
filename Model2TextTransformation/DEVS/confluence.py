from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass

@dataclass(repr=False)
class ConfluenceState:
	## The label of the state
	label = "idle"
	## All the vessels that have not yet been routed
	vessel_queue: list
	## The vessel that is currently being handled
	processing = None

	def __repr__(self):
		return f"ConfluenceState(label='{self.label}', len(vessel_queue)={len(self.vessel_queue)}, processing={self.processing})"

class Confluence(AtomicDEVS):
	"""
	A split/merge of multiple two-way Waterways and/or Canals. A parameter allows you to define how many Waterways
	and/or Canals converge at this Confluence. Sailing through a Confluence happens instantaneously. Arriving Vessels
	are handled in a FIFO (first-in-first-out) way. The Confluence uses the Vessel's destination to determine the
	desired output: when a Vessel arrives, it will be output on the Waterway or Canal that is closest to the destination
	Dock. When distances are approximately the same, the closest Lock is to be preferred on the trajectory. Furthermore,
	a Confluence can handle multiple Vessels at once.
	Hint: You may give the Anchorpoint a unique quay_id (see Dock) as well to simplify this logic. -> 0
	"""
	def __init__(self, name: str, number_of_waterways: int, routing: dict):
		super(Confluence, self).__init__(name)

		## Keeps track of which direction the out to use to get to a certain port
		self.routing = routing
		## The number of waterways (and confluence that meet at a confluence)
		self.number_of_waterways = number_of_waterways

		## The in- and out-ports of the confluence
		self.ship_in = []
		self.ship_out = []
		# Make the in and out ports
		for i in range(number_of_waterways):
			self.ship_in.append(self.addInPort(f"ship_in[{i}]"))
			self.ship_out.append(self.addOutPort(f"ship_out[{i}]"))

		# Initialize the internal state
		self.state = ConfluenceState([])

	def extTransition(self, inputs):
		keys = inputs.keys()
		intersection = list(set(self.ship_in) & set(keys))
		if len(intersection) != 0: # One of out ports is in the inputs
			vessel = inputs[intersection[0]] # Grab the first (there could be multiple :thinking:)
			self.state.vessel_queue.append(vessel)

			if not self.state.processing and self.state.vessel_queue:
				self.state.processing = self.state.vessel_queue.pop(0)
				self.state.label = "sending"
		return self.state

	def intTransition(self):
		# If there are still messages left to send, send them
		if self.state.vessel_queue:
			self.state.processing = self.state.vessel_queue.pop(0)
			self.state.label = "sending"
		else:
			self.state.processing = None
			self.state.label = "idle"  # And this weak and idle theme, No more yielding but a dream
		return self.state

	def outputFnc(self):
		# Find the best port given the destination of the vessel and send the current vessel that way
		best_port = self.ship_out[self.routing[self.state.processing.destination]]
		return {best_port: self.state.processing}

	def timeAdvance(self):
		return {"idle": INFINITY,
				"sending": 0}[self.state.label]

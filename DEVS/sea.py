from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY


class Sea(AtomicDEVS):
	"""
	The sea component.
	Since the end of the port is defined as "CP" the sea state is actually redundant but is added for completion.
	"""

	def __init__(self):
		super(Sea, self).__init__("Sea")
		self.state = "awash"
		self.ship_in = self.addInPort("ship_in")

	def extTransition(self, inputs):
		# Don't care about any incoming messages
		return self.state

	def timeAdvance(self):
		return INFINITY

from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass

@dataclass(repr=False)
class CPState:
	## The label of the state
	label = "idle"
	## All the vessels that have not yet been routed
	vessel_queue = []
	## The vessel that is currently being handled
	processing = None

	# -- For statistics --
	## The number of ships in the port
	ships_in_port: int
	## Keep track of the simulation time
	t_sim = 0.0
	## The arrival time of the vessels
	vessel_arrival: dict
	## The departure time of the vessels
	vessel_departure = {}
	## The vessels that have left the port
	departed_vessels = []
	## The number of vessels in the port at each update (note an update is when a vessel leaves or enters so this is
	##	 very precise measure of the changes.
	count_over_time: list

	def __repr__(self):
		return f"CPState(label='{self.label}', len(vessel_queue)={len(self.vessel_queue)}, processing={self.processing}, ships_in_port={self.ships_in_port})"

	def vessels_in_port_over_time(self):
		"""
		@Note: Should only be called after the simulation has concluded as this examines the state
		Can be used to generate:
		- Total number of vessels in the port at every hour in the simulation
		- Average number of vessels in the port.
		:return: Returns a list of tuples (t_sim, vessel_count)
		"""
		return self.count_over_time

	def port_time_per_vessel(self):
		"""
		@Note: Should only be called after the simulation has concluded as this examines the state
		Can be used to generate:
		- Average travel time for a vessel (from entering the port until leaving it again)
		:return: Returns a list of tuples (vessel, arrival_time, departure_time)
		"""
		return [(v, self.vessel_arrival[v.unique_id],  self.vessel_departure[v.unique_id]) for v in self.departed_vessels]


class CP(AtomicDEVS):
	"""
	Special version of the Confluence, marking the beginning and end of the port!
	Since this is the beginning and the end of the part this is the most natural place to collect a lot the statistics
	"""
	def __init__(self, name: str, number_of_waterways: int, routing: dict, ships_in_port=0, arrival_of_ships=None):
		super(CP, self).__init__(name)

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

		if arrival_of_ships is None:
			arrival_of_ships = {}
		# Initialize the internal state
		self.state = CPState(ships_in_port, arrival_of_ships, [(0,ships_in_port)])

	def extTransition(self, inputs):
		self.state.t_sim += self.elapsed  # Keep track of the time for the statistics

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
		self.state.t_sim += self.timeAdvance()  # Keep track of the time for the statistics

		# Collect the statistics. NOTE: We know that if the destination of the vessel is 0 that it is leaving
		if self.state.processing.destination == 0:
			# Vessel is leaving so record the departure time
			self.state.vessel_departure[self.state.processing.unique_id] = self.state.t_sim
			self.state.departed_vessels.append(self.state.processing)
			self.state.ships_in_port -= 1
		else:
			self.state.vessel_arrival[self.state.processing.unique_id] = self.state.t_sim
			self.state.ships_in_port += 1
		self.state.count_over_time.append((self.state.t_sim, self.state.ships_in_port))

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

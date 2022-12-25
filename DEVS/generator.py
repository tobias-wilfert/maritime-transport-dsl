import random
import numpy
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
# Our includes:
from events import Vessel
from vessel_names import vessel_names


class GeneratorState:
	""" The state of the Generator component. """

	def __init__(self, arrival_rate=None):
		## Keeps track of the simulation time.
		self.t_sim = 0.0
		## The next vessel that should be spawned.
		self.next_vessel = None
		## The delta till the vessel is spawned.
		self.next_IAT = INFINITY
		## Keeps track of how many ship have spawned and is also used for the unique Ship ID
		self.ship_counter = 0

		# For statistics
		self.type_count = [0, 0, 0, 0]  # Keeps track of how many ships have spawned per type.
		self.hour_count = []

		if arrival_rate is None:
			arrival_rate = [100, 120, 150, 175, 125, 50, 42, 68, 200, 220, 250, 245, 253, 236, 227, 246, 203, 43, 51,
							33, 143, 187, 164, 123]
		## The average number of Vessels arriving at the port on an hourly basis (24 hours = 1 day)
		self.arrival_rate = arrival_rate

	def __repr__(self):
		return f"GeneratorState(next_vessel={self.next_vessel}, next_IAT={self.next_IAT})"


class Generator(AtomicDEVS):
	""" Generates Vessels that arrive at the port, taking the probabilities from the Vessel description into account. """

	def __init__(self, seed: int = 0, arrival_rate=None):
		super(Generator, self).__init__("Generator")

		## Generate local instances of the random classes so that we avoid a global state
		self.random_state = random.Random(seed)
		self.random_numpy_state = numpy.random.RandomState(seed)

		## Add the out port for the ships
		self.ship_out = self.addOutPort("ship_out")

		## Initialize the internal state
		self.state = GeneratorState(arrival_rate)
		self.__generateVessel__()  # Generate the first Vessel

	def __generateVessel__(self):
		"""
		@Note: This should only be called from the init methode or intTransition as it changes the local state

		Generates and sets the vessel and the inter-arrival-time.
		:return: A vessel object, the inter-arrival-time.
		"""
		# Grab the vessel rate for the current hour
		vessel_rate_per_hour = self.state.arrival_rate[int(self.state.t_sim / 60) % 24]

		# Collect some interesting statistics
		if len(self.state.hour_count) - 1 != int(self.state.t_sim / 60):
			self.state.hour_count.append(0)
		self.state.hour_count[-1] += 1

		# NOTE: This will return hours so need to multipy with 60 to get minutes
		# Set the next intern arrival time
		self.state.next_IAT = self.random_numpy_state.exponential(scale=1 / vessel_rate_per_hour) * 60
		# self.state.next_IAT = (1 / vessel_rate_per_hour) * 60 TODO: To force same IAT

		# Random value to determine the type of the vessel
		type_var = int(self.random_state.uniform(0, 999))
		# Random value to determine the name of the vessel
		name_var = int(self.random_state.uniform(0, len(vessel_names) - 1))

		vessel_type = None
		if type_var < 280:
			self.state.type_count[0] += 1  # Used for statistics
			vessel_type = "CrudeOilTanker"
		elif type_var < 280 + 220:
			self.state.type_count[1] += 1  # Used for statistics
			vessel_type = "BulkCarrier"
		elif type_var < 280 + 220 + 330:
			self.state.type_count[2] += 1  # Used for statistics
			vessel_type = "TugBoat"
		else:
			self.state.type_count[3] += 1  # Used for statistics
			vessel_type = "SmallCargoFreighter"

		# Set the next vessel
		self.state.next_vessel = Vessel(vessel_type, self.state.ship_counter, vessel_names[name_var], -1)
		self.state.ship_counter += 1  # Update the ship  counter since we just "made" a ship

	def intTransition(self):
		""" :return: Returns the updated state after the internal transition. """
		self.state.t_sim += self.timeAdvance()  # Update the internal simulation timer
		self.__generateVessel__()
		# self.state.next_IAT = INFINITY # TODO: Spawn only one ship for debugging
		return self.state  # Return the new state

	def outputFnc(self):
		""" :return: Returns the vessel on the ship_out port. """
		return {self.ship_out: self.state.next_vessel}

	def timeAdvance(self):
		""" :return: The inter arrival time till the next vessel. """
		return self.state.next_IAT

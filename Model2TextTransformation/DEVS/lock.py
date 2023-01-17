from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from dataclasses import dataclass

@dataclass(repr=False)
class LockState:
	## The simulation time
	t_sim = 0.0
	## The level of the lock
	level = "LOW"  # or HIGH
	## The id of the lock
	id: str
	## Encodes the state of the Lock
	label = "OPEN"  # (OPENING, OPEN, WASHING, CLOSING)
	## The time until a state change
	remaining_time_global = 0
	## The time until the next vessel can leave the lock, INFINITY if none can leave ATM
	remaining_time_vessel = INFINITY
	## Vessels queuing for the lock on the low side
	vessel_queue_low: list
	## Vessels queuing for the lock on the high side
	vessel_queue_high: list
	## The vessels that are in the lock with direction low
	vessel_in_lock_low: list
	## The vessels that are in the lock with direction high
	vessel_in_lock_high: list
	## The vessel that is currently being processed
	processing = None

	# -- For statistics --
	remaining_capacity_per_change: list
	remaining_capacity_over_time: list

	# Determined by the id of the lock
	washing_duration: int = 0
	lock_shift_interval: int = 0
	opening_closing_duration: int = 0
	open_duration: int = 0
	area: float = 0.0
	## Keeps track of how much space there is still left in the lock
	remaining_capacity = 0

	def __post_init__(self):
		if self.id == "Lock A":
			self.washing_duration = 20
			self.lock_shift_interval = 60
			self.opening_closing_duration = 7
			self.area = 62500
		elif self.id == "Lock B":
			self.washing_duration = 12
			self.lock_shift_interval = 45
			self.opening_closing_duration = 5
			self.area = 34000
		elif self.id == "Lock C":
			self.washing_duration = 8
			self.lock_shift_interval = 30
			self.opening_closing_duration = 5
			self.area = 25650
		else:
			raise TypeError(f"ID: {self.id} is not a valid Lock ID")
		self.open_duration = self.lock_shift_interval - 2*self.opening_closing_duration - self.washing_duration
		self.remaining_time_global = self.open_duration
		self.remaining_capacity = self.area
		self.remaining_capacity_over_time = [(0, self.area)]

	def __repr__(self):
		return f"LockState(id={self.id}, level={self.level}, label={self.label}, remaining_capacity={self.remaining_capacity}, len(vessel_queue_low)={len(self.vessel_queue_low)}, len(vessel_queue_high)={len(self.vessel_queue_high)}, len(vessel_in_lock_low)={len(self.vessel_in_lock_low)}, len(vessel_in_lock_high)={len(self.vessel_in_lock_high)})"

	def number_of_empty_transitions(self):
		"""
		@Note: Should only be called after the simulation has concluded as this examines the state
		:return: The number of times the lock changed state while empty
		"""
		return self.remaining_capacity_per_change.count(self.area)

	def capacity_per_change(self):
		"""
		@Note: Should only be called after the simulation has concluded as this examines the state
		:return: The capacity left in the lock per state change
		"""
		return self.remaining_capacity_per_change

	def get_remaining_capacity_over_time(self):
		"""
		@Note: Should only be called after the simulation has concluded as this examines the state
		:return: The capacity left in the lock per state change
		"""
		return self.remaining_capacity_over_time

class Lock(AtomicDEVS):
	def __init__(self, name: str):
		super(Lock, self).__init__(name)
		# Add the output and input ports
		self.ship_in_low = self.addInPort("ship_in_low")
		self.ship_out_low = self.addOutPort("ship_out_low")
		self.ship_in_high = self.addInPort("ship_in_high")
		self.ship_out_high = self.addOutPort("ship_out_high")
		# Initialize the internal state
		self.state = LockState(name, [], [], [], [], [], [])

	def extTransition(self, inputs):
		self.state.t_sim += self.elapsed # Update the t_sim
		# Update the counters
		self.state.remaining_time_global -= self.elapsed
		self.state.remaining_time_vessel -= self.elapsed

		if self.ship_in_low in inputs:
			vessel = inputs[self.ship_in_low]
			# It could be that the gate is open and that there is capacity if that is the case we need to insert the boat
			if self.state.level == "LOW" and self.state.label == "OPEN" and self.state.remaining_capacity > vessel.area:
				self.state.vessel_in_lock_low.append(vessel)
				self.state.remaining_capacity -= vessel.area
				# Now that new vessel has entered check how much capacity there is left
				self.state.remaining_capacity_over_time.append((self.state.t_sim, self.state.remaining_capacity))
			else:
				self.state.vessel_queue_low.append(vessel)

		if self.ship_in_high in inputs:
			vessel = inputs[self.ship_in_high]
			# It could be that the gate is open and that there is capacity if that is the case we need to insert the boat
			if self.state.level == "HIGH" and self.state.label == "OPEN" and self.state.remaining_capacity > vessel.area:
				self.state.vessel_in_lock_high.append(vessel)
				self.state.remaining_capacity -= vessel.area
				# Now that new vessel has entered check how much capacity there is left
				self.state.remaining_capacity_over_time.append((self.state.t_sim, self.state.remaining_capacity))
			else:
				self.state.vessel_queue_high.append(vessel)
		return self.state

	def intTransition(self):
		self.state.t_sim += self.timeAdvance()  # Update the t_sim

		# Update the counters
		self.state.remaining_time_global -= self.timeAdvance()
		self.state.remaining_time_vessel -= self.timeAdvance()

		# A State change
		if self.state.remaining_time_global == 0:
			# Check what the current state is
			if self.state.label == "OPEN":
				self.state.label = "CLOSING"
				self.state.remaining_time_global = self.state.opening_closing_duration
				# Collect statistics, this only indicates it at the changes
				self.state.remaining_capacity_per_change.append(self.state.remaining_capacity)
			elif self.state.label == "CLOSING":
				self.state.label = "WASHING"
				self.state.remaining_time_global = self.state.washing_duration
			elif self.state.label == "WASHING":
				self.state.label = "OPENING"
				self.state.remaining_time_global = self.state.opening_closing_duration
			elif self.state.label == "OPENING":
				self.state.label = "OPEN"
				self.state.remaining_time_global = self.state.open_duration
				self.state.remaining_capacity = self.state.area # Reset the capacity

				if self.state.level == "LOW":
					# TODO: Fill up the capacity with all the vessels available
					temp = []
					for vessel in self.state.vessel_queue_high:
						if vessel.area < self.state.remaining_capacity:
							self.state.vessel_in_lock_high.append(vessel)
							self.state.remaining_capacity -= vessel.area
						else:
							temp.append(vessel)
					self.state.vessel_queue_high = temp

					if self.state.vessel_in_lock_low:
						self.state.processing = self.state.vessel_in_lock_low.pop(0)
						self.state.remaining_time_vessel = 0  # Reset the counter
					self.state.level = "HIGH"  # Flip the state
				else:
					temp = []
					for vessel in self.state.vessel_queue_low:
						if vessel.area < self.state.remaining_capacity:
							self.state.vessel_in_lock_low.append(vessel)
							self.state.remaining_capacity -= vessel.area
						else:
							temp.append(vessel)
					self.state.vessel_queue_low = temp

					if self.state.vessel_in_lock_high:
						self.state.processing = self.state.vessel_in_lock_high.pop(0)
						self.state.remaining_time_vessel = 0  # Reset the counter
					self.state.level = "LOW" # Flip the state

				# Now that new vessels might have entered check how much capacity there is left
				self.state.remaining_capacity_over_time.append((self.state.t_sim, self.state.remaining_capacity))
			else:
				raise TypeError(f"State: {self.state.label} is not a state for Lock")
		# New vessel can leave, check if there are any vessels left
		else:
			if self.state.level == "LOW":
				if self.state.vessel_in_lock_high:
					self.state.processing = self.state.vessel_in_lock_high.pop(0)
					self.state.remaining_time_vessel = 0.5
				else:
					self.state.remaining_time_vessel = INFINITY
					self.state.processing = None
			else:
				if self.state.vessel_in_lock_low:
					self.state.processing = self.state.vessel_in_lock_low.pop(0)
					self.state.remaining_time_vessel = 0.5
				else:
					self.state.remaining_time_vessel = INFINITY
					self.state.processing = None
		return self.state

	def outputFnc(self):
		if self.state.processing:
			# Output the vessel on the correct port
			port = self.ship_out_low if self.state.level == "LOW" else self.ship_out_high
			# Only output in special case
			return {port: self.state.processing}
		return {}

	def timeAdvance(self):
		# Either a global state change or the departure of a vessel, what ever happens firsts
		return min(self.state.remaining_time_global, self.state.remaining_time_vessel)

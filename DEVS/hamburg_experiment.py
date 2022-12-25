from pypdevs.simulator import Simulator
import matplotlib.pyplot as plt
import random
# Our includes
from hamburg import Network
from vessel_names import vessel_names
from events import Vessel

# -- Global variables --
SIMULATION_TIME_IN_HOURS = 168
PATH = "/plots_hamburg/"
TRACE_FILE_NAME = "." + PATH + "trace.txt"  # If none then it is printed to the console

# -- Functions to do the statistics
def analyze_avg_travel_time_for_a_vessel(model):
	time_per_vessel = model.Confluence_26.state.port_time_per_vessel()
	time_per_crude_oil_tanker = [(a,d) for v,a,d in time_per_vessel if v.type == "CrudeOilTanker"]
	time_per_bulk_carrier = [(a,d) for v,a,d in time_per_vessel if v.type == "BulkCarrier"]
	time_per_tug_boat = [(a,d) for v,a,d in time_per_vessel if v.type == "TugBoat"]
	time_per_small_cargo_freighter = [(a,d) for v,a,d in time_per_vessel if v.type == "SmallCargoFreighter"]

	# Output the stats to the console
	avg_time_per_vessel = sum(d-a for v,a,d in time_per_vessel) / len(time_per_vessel) if len(time_per_vessel) else 0
	print(f"| Avg. travel time for a vessel (in the port): {avg_time_per_vessel} minutes")

	# Plot the data for each of the vessel types
	avg_t_crude_oil_tanker = sum(d-a for a,d in time_per_crude_oil_tanker) / len(time_per_crude_oil_tanker) if len(time_per_crude_oil_tanker) else 0
	avg_t_bulk_carrier = sum(d-a for a,d in time_per_bulk_carrier) / len(time_per_bulk_carrier) if len(time_per_bulk_carrier) else 0
	avg_t_tug_boat = sum(d-a for a,d in time_per_tug_boat) / len(time_per_tug_boat) if len(time_per_tug_boat) else 0
	avg_t_small_cargo_freighter = sum(d-a for a,d in time_per_small_cargo_freighter) / len(time_per_small_cargo_freighter) if len(time_per_small_cargo_freighter) else 0

	print(f"| ... for CrudeOilTanker: {avg_t_crude_oil_tanker} minutes")
	print(f"| ... for BulkCarrier: {avg_t_bulk_carrier} minutes")
	print(f"| ... for TugBoat: {avg_t_tug_boat} minutes")
	print(f"| ... for SmallCargoFreighter: {avg_t_small_cargo_freighter} minutes")
	print("+")

	# Make the graph
	plt.figure(figsize=(10,10))  # Make the plot big

	# Plot the different vessels in different colour
	plt.scatter([d for a, d in time_per_crude_oil_tanker], [d - a for a, d in time_per_crude_oil_tanker], color="yellowgreen", marker='.', label='Time per CrudeOilTanker')
	plt.scatter([d for a, d in time_per_bulk_carrier], [d - a for a, d in time_per_bulk_carrier], color="orange", marker='.', label='Time per BulkCarrier')
	plt.scatter([d for a, d in time_per_tug_boat], [d - a for a, d in time_per_tug_boat], color="blue", marker='.', label='Time per TugBoat')
	plt.scatter([d for a, d in time_per_small_cargo_freighter], [d - a for a, d in time_per_small_cargo_freighter], color="orchid", marker='.', label='Time per SmallCargoFreighter')
	plt.axhline(y=avg_time_per_vessel, color= 'red', label='Avg. time')

	# Add the metadata to the graph
	plt.legend(loc="upper left")
	plt.title("Average travel time for a vessel (from entering the port until leaving it again)")
	plt.xlabel(f"Time of port departure (minutes)")
	plt.ylabel("Time spend in port (minutes)")
	plt.savefig(f".{PATH}avg_travel_time_for_vessel_in_port_t{SIMULATION_TIME_IN_HOURS*60}.png")
	plt.show()

	# Make the metagraph
	fig,ax = plt.subplots(figsize=(10,10))
	ax.eventplot([[d - a for a, d in time_per_crude_oil_tanker],
				  [d - a for a, d in time_per_bulk_carrier],
				  [d - a for a, d in time_per_tug_boat],
				  [d - a for a, d in time_per_small_cargo_freighter]], orientation="vertical", lineoffsets=[2,4,6,8], colors=["yellowgreen", "orange", "blue", "orchid"], linewidth=0.75)

	plt.title("Travel time for a vessel (per vessel type)")
	plt.ylabel("Time spend in port (minutes)")
	plt.xlabel(f"Vessel type")
	plt.xticks([2,4,6,8], ["CrudeOilTanker", "BulkCarrier", "TugBoat", "SmallCargoFreighter"])
	plt.savefig(f".{PATH}travel_time_for_vessel_t{SIMULATION_TIME_IN_HOURS*60}.png")
	plt.show()

def analyze_waiting_time_in_anchor_point(model):
	avg_time = model.Anchorpoint_42.state.avg_waiting_time()
	print(f"| Average waiting time for a vessel in the Anchorpoint: {avg_time} minutes")
	print("+")

	time_per_vessel = model.Anchorpoint_42.state.time_per_vessel()
	# Make a plot to show the behaviour overtime
	# Make the graph
	plt.figure(figsize=(10,10))  # Make the plot big

	plt.scatter([d for v, d, a in time_per_vessel], [d - a for  v,d,a in time_per_vessel], marker='.', label='Time per Vessel')
	plt.axhline(y=avg_time, color= 'red', label='Avg. time')

	# Add the metadata to the graph
	plt.legend(loc="upper left")
	plt.title("Average waiting time for a vessel in the Anchorpoint.")
	plt.xlabel(f"Time of port departure (minutes)")
	plt.ylabel("Time waited (minutes)")
	plt.savefig(f".{PATH}avg_waiting_time_in_anchorpoint_t{SIMULATION_TIME_IN_HOURS*60}.png")
	plt.show()

def analyze_avg_number_of_vessels_in_port(model):
	#print(f"Vessels in port: {model.cp.state.vessels_in_port_over_time()}")
	vessels_in_port = model.Confluence_26.state.vessels_in_port_over_time()
	avg_vessels_in_port = sum(c for t,c in vessels_in_port)/len(vessels_in_port) if len(vessels_in_port) else 0
	print(f"| Average number of vessels in the port.: {avg_vessels_in_port}")
	print("+")

	# Make a plot to show the behaviour overtime
	# Make the graph
	plt.figure(figsize=(10, 10))  # Make the plot big

	plt.scatter([t for t, c in vessels_in_port], [c for t, c in vessels_in_port], marker='.', label="Vessel count")
	plt.axhline(y=avg_vessels_in_port, color='red', label='Avg. number')

	# Add the metadata to the graph
	plt.legend(loc="upper left")
	plt.title("Average number of vessels in the port.")
	plt.xlabel(f"Simulation time (minutes)")
	plt.ylabel("Number of vessels")
	plt.savefig(f".{PATH}avg_number_of_vessels_in_port_t{SIMULATION_TIME_IN_HOURS * 60}.png")
	plt.show()

def analyze_number_of_vessels_in_port_per_hour(model):
	# Make a bar chart for this?
	# Check at the beginning of each hour how many vessels are in the port
	vessel_count_each_hour = []
	last_hour = -1
	for t_sim, count in model.Confluence_26.state.vessels_in_port_over_time():
		# If the time is not the last hour then append a new item
		cur_hour = int(t_sim/60)
		if cur_hour != last_hour:
			# Check if we skipped number
			if last_hour != -1:
				while last_hour < cur_hour-1:
					vessel_count_each_hour.append(vessel_count_each_hour[-1])
					last_hour += 1
			vessel_count_each_hour.append(count)
			last_hour = cur_hour

	# Make the graph
	plt.figure(figsize=(10, 10))  # Make the plot big
	plt.bar(range(len(vessel_count_each_hour)), vessel_count_each_hour, width=1, edgecolor="white", linewidth=0.7)

	plt.title("Total number of vessels in the port at every hour in the simulation.")
	plt.xlabel(f"Simulation time (hours)")
	plt.ylabel("Number of vessels")
	plt.savefig(f".{PATH}number_of_vessels_in_port_t{SIMULATION_TIME_IN_HOURS * 60}.png")
	plt.show()

def analyze_idle_time_per_lock(lock):
	# The time that there is no vessel in the lock
	remaining_capacity = lock.state.get_remaining_capacity_over_time()
	remaining_capacity.append((SIMULATION_TIME_IN_HOURS*60, -1))
	idle_count = 0
	idle_segments = []
	last_t, last_c = remaining_capacity[0]
	for i in range(1, len(remaining_capacity)):
		cur_t, cur_c = remaining_capacity[i]
		if last_c != cur_c: # We have a delta
			if last_c == lock.state.area:
				idle_count += (cur_t - last_t)
				idle_segments.append(cur_t - last_t)
			last_c = cur_c
			last_t = cur_t

	avg_idle = sum(idle_segments) / len(idle_segments) if len(idle_segments) else 0
	print(f"| Idle time for {lock.state.id}: {idle_count} minutes")
	print(f"| Avg. idle duration of {lock.state.id}: {avg_idle} minutes")

def analyze_idle_state_changes(lock):
	print(f"| Number of idle state changes {lock.state.id}: {lock.state.number_of_empty_transitions()}/{len(lock.state.capacity_per_change())}")

def analyze_remaining_capacity_over_time(lock):
	# Make plot over time (NOTE we take a more granular time than hour)
	capacity = lock.state.get_remaining_capacity_over_time()

	# Make the graph
	plt.figure(figsize=(10,10))  # Make the plot big

	plt.scatter([t for t,c in capacity], [c for t,c in capacity], marker='.', label='Remaining capacity')
	plt.axhline(y=lock.state.area, color= 'red', label='Lock area')

	# Add the metadata to the graph
	plt.legend(loc="upper right")
	plt.title(f"Remaining capacity for {lock.state.id} over time.")
	plt.xlabel(f"Remaining capacity (m^2)")
	plt.ylabel("Simulation time (minutes)")
	plt.savefig(f".{PATH}{lock.state.id}_remaining_capacity_t{SIMULATION_TIME_IN_HOURS*60}.png")
	plt.show()

def analyze_vessel_spawn_rate(model):
	print("| The number of Watercraft that we would expect to spawn (rate/hour):")
	print(
		f"| {[100, 120, 150, 175, 125, 50, 42, 68, 200, 220, 250, 245, 253, 236, 227, 246, 203, 43, 51, 33, 143, 187, 164, 123]}")
	print(f"| Observed rate:")
	count = 24
	while count < len(model.Generator_14.state.hour_count):
		print(f" {model.Generator_14.state.hour_count[count - 24: count]}")
		count += 24
	print(f" {model.Generator_14.state.hour_count[count - 24:]}")
	print("+")

def analyze_vessel_spawn_per_type(model):
	print(f"| The spawn probability per type [28%, 22%, 33%, 17%]")
	print(f"| {[x / model.Generator_14.state.ship_counter for x in model.Generator_14.state.type_count]}")
	print("+")

def initialize_ships(model, n=100, seed=0):
	random_state = random.Random(seed)

	for i in range(n):
		type_var = int(random_state.uniform(0, 999))
		name_var = int(random_state.uniform(0, len(vessel_names) - 1))
		time = int(random_state.uniform(0, 36*60))
		dock = int(random_state.uniform(1, 8))  # What are the odds of this making more than 50 for 1?

		vessel_type = None
		if type_var < 280:
			vessel_type = "CrudeOilTanker"
		elif type_var < 280 + 220:
			vessel_type = "BulkCarrier"
		elif type_var < 280 + 220 + 330:
			vessel_type = "TugBoat"
		else:
			vessel_type = "SmallCargoFreighter"

		# Make the vessel
		vessel = Vessel(vessel_type, model.Generator_14.state.ship_counter, vessel_names[name_var], 0)
		model.Generator_14.state.ship_counter += 1 # Update the generator counter
		model.Confluence_26.state.vessel_arrival[vessel.unique_id] = 0 # Le the CP know
		model.ControlTower_3.state.idle_docks.remove(dock)
		# Assign the vessel to the dock
		if dock == 1:
			model.Dock_60.state.vessels.append((vessel, time))
		elif dock == 2:
			model.Dock_61.state.vessels.append((vessel, time))
		elif dock == 3:
			model.Dock_98.state.vessels.append((vessel, time))
		elif dock == 4:
			model.Dock_99.state.vessels.append((vessel, time))
		elif dock == 5:
			model.Dock_100.state.vessels.append((vessel, time))
		elif dock == 6:
			model.Dock_129.state.vessels.append((vessel, time))
		elif dock == 7:
			model.Dock_130.state.vessels.append((vessel, time))
		elif dock == 8:
			model.Dock_131.state.vessels.append((vessel, time))

	model.Confluence_26.state.ships_in_port = n

if __name__ == '__main__':
	model = Network()

	# -- Make any setup changes to Model --
	# initialize_ships(model, seed=0)

	# Need to update the dock count in the CP
	model.ControlTower_3.state.idle_docks = sorted([1,2,3,4,5,6,7] * 50)

	# --  Simulate the model --
	sim = Simulator(model)
	sim.setClassicDEVS()
	sim.setVerbose(TRACE_FILE_NAME)
	sim.setTerminationTime(SIMULATION_TIME_IN_HOURS * 60)  # Our base unit of simulation is the minute
	sim.simulate()


	# -- Collect and display the statistics --
	print('+' + '-' * 60 + '+')
	print("| Statistics:")
	print('+' + '-' * 60 + '+')
	# Additional:
	# Required:
	# 1- Average travel time for a vessel (from entering the port until leaving it again).
	analyze_avg_travel_time_for_a_vessel(model)
	# 2- Average waiting time for a vessel in the Anchorpoint.
	analyze_waiting_time_in_anchor_point(model)
	# 3- Average number of vessels in the port.
	analyze_avg_number_of_vessels_in_port(model)
	# 4- Total number of vessels in the port at every hour in the simulation (create a plot for this statistic).
	analyze_number_of_vessels_in_port_per_hour(model)
	# 5- Average idle time for each Lock (i.e., the time that there are no vessels inside).
	analyze_idle_time_per_lock(model.Lock_37)
	#analyze_idle_time_per_lock(model.Lock_38)
	analyze_idle_time_per_lock(model.Lock_39)
	print("+")
	# 6- How often a Lock changed state without it actually containing ships.
	analyze_idle_state_changes(model.Lock_37)
	#analyze_idle_state_changes(model.Lock_38)
	analyze_idle_state_changes(model.Lock_39)
	print("+")
	# 7- Remaining capacity (surface area) for each Lock at every hour in the simulation (create a plot for this statistic).
	analyze_remaining_capacity_over_time(model.Lock_37)
	#analyze_remaining_capacity_over_time(model.Lock_38)
	analyze_remaining_capacity_over_time(model.Lock_39)

	print('+' + '-' * 60 + '+')
	print("| More statistics:")
	print('+' + '-' * 60 + '+')

	# Check that the spawn vessel rate (per hour) matches what we expect
	# analyze_vessel_spawn_rate(model)
	# Check that the different types are spawned in the correct amount
	analyze_vessel_spawn_per_type(model)

	print(f"| The simulation time as seen by the generator: {model.Generator_14.state.t_sim}")
	print(f"| The number of ships that the generator spawned: {model.Generator_14.state.ship_counter}")
	print(f"| The number of ships consumed: {len(model.Confluence_26.state.departed_vessels)}")
	print('+' + '-' * 60 + '+')


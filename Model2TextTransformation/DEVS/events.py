from dataclasses import dataclass


@dataclass()
class Vessel:
	"""
	Identifies a vessel/ship travelling through the system can have type:
	 - Crude Oil Tanker (28%), Bulk Carrier (22%), Tug Boat (33%), Small Cargo Freighter (17%)
	"""
	## The type of the vessel determines the area and velocity
	type: str
	## Unique ID for the vessel
	unique_id: int
	## Name of the vessel
	name: str
	## Destination of the vessel
	destination: int
	# Determined by the type of the vessel
	area: float = 0.0  # unit: Meters^2
	avg_velocity: float = 0.0  # unit: Knots
	max_velocity: float = 0.0  # unit: Knots

	def __post_init__(self):
		if self.type == "CrudeOilTanker":
			self.area = 11007.0
			self.avg_velocity = 10.7
			self.max_velocity = 15.4
		elif self.type == "BulkCarrier":
			self.area = 5399.0
			self.avg_velocity = 12
			self.max_velocity = 15.6
		elif self.type == "TugBoat":
			self.area = 348.0
			self.avg_velocity = 7.8
			self.max_velocity = 10.6
		elif self.type == "SmallCargoFreighter":
			self.area = 1265.0
			self.avg_velocity = 6.4
			self.max_velocity = 9.8
		else:
			raise TypeError(f"Type: {self.type} is not a valid Vessel type")


@dataclass(frozen=True)
class PortEntryRequest:
	"""
	Indicates a message sent from the Anchorpoint to the ControlTower, informing the latter that a ship with a certain
	identification number would like to enter the port.
	"""
	ship_id: int


@dataclass(frozen=True)
class PortEntryPermission:
	"""
	Dual of the PortEntryRequest. This is a message sent from the ControlTower to the Anchorpoint, informing the latter
	that a ship with a certain identification number is allowed to enter the port and can dock at a specified quay.
	"""
	ship_id: int
	quay_id: int


@dataclass(frozen=True)
class PortDepartureRequest:
	"""
	Sent by a Dock to the ControlTower, identifying that a certain Vessel has left a specific Dock, making room for
	another ship to arrive.
	"""
	ship_id: int
	quay_id: int

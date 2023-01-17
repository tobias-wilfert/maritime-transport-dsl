from pypdevs.DEVS import CoupledDEVS
# Our includes:
from anchorpoint import Anchorpoint
from canal import Canal
from confluence import Confluence
from controltower import ControlTower
from cp import CP
from dock import Dock
from generator import Generator
from lock import Lock
from sea import Sea
from waterway import Waterway


class Network(CoupledDEVS):
  """ A Coupled DEVS model of the network. """

  def __init__(self):
    super(Network, self).__init__("Network")

    # Make all the components
    self.Generator_14 = self.addSubModel(Generator())  # Note: Generator has a default name
    self.Anchorpoint_42 = self.addSubModel(Anchorpoint())  # Note: Anchorpoint has a default name
    self.ControlTower_3 = self.addSubModel(ControlTower())  # Note: ControlTower has a default name
    self.Sea_4 = self.addSubModel(Sea())  # Note: Sea has a default name
    
    # Docks
    self.Dock_60 = self.addSubModel(Dock(int("d1"[-1])))
    self.Dock_131 = self.addSubModel(Dock(int("d8"[-1])))
    self.Dock_61 = self.addSubModel(Dock(int("d2"[-1])))
    self.Dock_130 = self.addSubModel(Dock(int("d7"[-1])))
    self.Dock_100 = self.addSubModel(Dock(int("d5"[-1])))
    self.Dock_99 = self.addSubModel(Dock(int("d4"[-1])))
    self.Dock_98 = self.addSubModel(Dock(int("d3"[-1])))
    self.Dock_129 = self.addSubModel(Dock(int("d6"[-1])))

    # Locks
    # Also need to fix the naming here
    self.Lock_37 = self.addSubModel(Lock("Lock " + "LA"[-1]))
    self.Lock_38 = self.addSubModel(Lock("Lock " + "LB"[-1]))
    self.Lock_39 = self.addSubModel(Lock("Lock " + "LC"[-1]))

    # Need to convert these values to meters
    # Waterways (make 2 since they are only singly linked in our model)
    self.Waterway_17_A = self.addSubModel(Waterway("w_K_c1_A", 47.52*1000))
    self.Waterway_17_B = self.addSubModel(Waterway("w_K_c1_B", 47.52*1000))
    self.Waterway_18_A = self.addSubModel(Waterway("w_c1_S_A", 30.85*1000))
    self.Waterway_18_B = self.addSubModel(Waterway("w_c1_S_B", 30.85*1000))
    self.Waterway_29_A = self.addSubModel(Waterway("w_CP_c2_A", 4.7*1000))
    self.Waterway_29_B = self.addSubModel(Waterway("w_CP_c2_B", 4.7*1000))
    self.Waterway_25_A = self.addSubModel(Waterway("w_c1_CP_A", 68.54*1000))
    self.Waterway_25_B = self.addSubModel(Waterway("w_c1_CP_B", 68.54*1000))
    self.Waterway_30_A = self.addSubModel(Waterway("w_CP_LA_A", 2.1*1000))
    self.Waterway_30_B = self.addSubModel(Waterway("w_CP_LA_B", 2.1*1000))
    self.Waterway_110_A = self.addSubModel(Waterway("w_c2_LC_A", 1.0*1000))
    self.Waterway_110_B = self.addSubModel(Waterway("w_c2_LC_B", 1.0*1000))
      
    # Canal (make 2 since they are only singly linked in our model)
    self.Canal_59_A = self.addSubModel(Canal("c_c5_d2_A", 1.13*1000))
    self.Canal_59_B = self.addSubModel(Canal("c_c5_d2_B", 1.13*1000))
    self.Canal_124_A = self.addSubModel(Canal("c_c6_LB_A", 0.89*1000))
    self.Canal_124_B = self.addSubModel(Canal("c_c6_LB_B", 0.89*1000))
    self.Canal_84_A = self.addSubModel(Canal("c_LC_c4_A", 1.08*1000))
    self.Canal_84_B = self.addSubModel(Canal("c_LC_c4_B", 1.08*1000))
    self.Canal_54_A = self.addSubModel(Canal("c_LA_c3_A", 0.8*1000))
    self.Canal_54_B = self.addSubModel(Canal("c_LA_c3_B", 0.8*1000))
    self.Canal_56_A = self.addSubModel(Canal("c_c3_c5_A", 2.39*1000))
    self.Canal_56_B = self.addSubModel(Canal("c_c3_c5_B", 2.39*1000))
    self.Canal_55_A = self.addSubModel(Canal("c_d1_c3_A", 1.89*1000))
    self.Canal_55_B = self.addSubModel(Canal("c_d1_c3_B", 1.89*1000))
    self.Canal_58_A = self.addSubModel(Canal("c_c5_d4_A", 5.7*1000))
    self.Canal_58_B = self.addSubModel(Canal("c_c5_d4_B", 5.7*1000))
    self.Canal_81_A = self.addSubModel(Canal("c_c4_d3_A", 1.86*1000))
    self.Canal_81_B = self.addSubModel(Canal("c_c4_d3_B", 1.86*1000))
    self.Canal_83_A = self.addSubModel(Canal("c_c4_d5_A", 1.68*1000))
    self.Canal_83_B = self.addSubModel(Canal("c_c4_d5_B", 1.68*1000))
    self.Canal_82_A = self.addSubModel(Canal("c_c4_d4_A", 1.3*1000))
    self.Canal_82_B = self.addSubModel(Canal("c_c4_d4_B", 1.3*1000))
    self.Canal_125_A = self.addSubModel(Canal("c_c7_c6_A", 1.24*1000))
    self.Canal_125_B = self.addSubModel(Canal("c_c7_c6_B", 1.24*1000))
    self.Canal_126_A = self.addSubModel(Canal("c_c6_d8_A", 2.4*1000))
    self.Canal_126_B = self.addSubModel(Canal("c_c6_d8_B", 2.4*1000))
    self.Canal_116_A = self.addSubModel(Canal("c_c2_LB_A", 3.14*1000))
    self.Canal_116_B = self.addSubModel(Canal("c_c2_LB_B", 3.14*1000))
    self.Canal_127_A = self.addSubModel(Canal("c_c7_d7_A", 1.07*1000))
    self.Canal_127_B = self.addSubModel(Canal("c_c7_d7_B", 1.07*1000))
    self.Canal_128_A = self.addSubModel(Canal("c_c7_d6_A", 1.37*1000))
    self.Canal_128_B = self.addSubModel(Canal("c_c7_d6_B", 1.37*1000))
    
    # Need to do some hacking here
    self.Confluence_107 = self.addSubModel(Confluence("c2", 3+1, {
0: 2, int("d1"[-1]):2, int("d8"[-1]):0, int("d2"[-1]):1, int("d7"[-1]):0, int("d5"[-1]):1, int("d4"[-1]):1, int("d3"[-1]):1, int("d6"[-1]):0, }))
    # Need to do some hacking here
    self.Confluence_80 = self.addSubModel(Confluence("c4", 5+1, {
0: 0, int("d1"[-1]):4, int("d8"[-1]):0, int("d2"[-1]):4, int("d7"[-1]):0, int("d5"[-1]):3, int("d4"[-1]):1, int("d3"[-1]):2, int("d6"[-1]):0, }))
    self.Confluence_26 = self.addSubModel(CP("CP", 3, { 
0: 2, int("d1"[-1]):1, int("d8"[-1]):0, int("d2"[-1]):1, int("d7"[-1]):0, int("d5"[-1]):0, int("d4"[-1]):0, int("d3"[-1]):0, int("d6"[-1]):0, }))  # Note: this is a special case
    # Need to do some hacking here
    self.Confluence_45 = self.addSubModel(Confluence("c1", 2+1, {
0: 0, int("d1"[-1]):1, int("d8"[-1]):1, int("d2"[-1]):1, int("d7"[-1]):1, int("d5"[-1]):1, int("d4"[-1]):1, int("d3"[-1]):1, int("d6"[-1]):1, }))
    # Need to do some hacking here
    self.Confluence_57 = self.addSubModel(Confluence("c5", 3+1, {
0: 2, int("d1"[-1]):2, int("d8"[-1]):0, int("d2"[-1]):1, int("d7"[-1]):0, int("d5"[-1]):0, int("d4"[-1]):0, int("d3"[-1]):0, int("d6"[-1]):0, }))
    # Need to do some hacking here
    self.Confluence_123 = self.addSubModel(Confluence("c7", 3+1, {
0: 0, int("d1"[-1]):0, int("d8"[-1]):0, int("d2"[-1]):0, int("d7"[-1]):2, int("d5"[-1]):0, int("d4"[-1]):0, int("d3"[-1]):0, int("d6"[-1]):1, }))
    # Need to do some hacking here
    self.Confluence_53 = self.addSubModel(Confluence("c3", 3+1, {
0: 2, int("d1"[-1]):1, int("d8"[-1]):2, int("d2"[-1]):0, int("d7"[-1]):2, int("d5"[-1]):0, int("d4"[-1]):0, int("d3"[-1]):0, int("d6"[-1]):2, }))
    # Need to do some hacking here
    self.Confluence_122 = self.addSubModel(Confluence("c6", 3+1, {
0: 2, int("d1"[-1]):2, int("d8"[-1]):1, int("d2"[-1]):2, int("d7"[-1]):0, int("d5"[-1]):2, int("d4"[-1]):2, int("d3"[-1]):2, int("d6"[-1]):0, }))

    # Connect the PortDepartureRequests
    self.connectPorts(self.Dock_61.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_98.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_99.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_100.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_60.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_131.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_130.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_129.message_out ,self.ControlTower_3.message_in)
    # Connect the PortEntryRequest
    self.connectPorts(self.Anchorpoint_42.message_out ,self.ControlTower_3.message_in)
    # Connect the PortEntryPermission
    self.connectPorts(self.ControlTower_3.message_out ,self.Anchorpoint_42.message_in)

    # Connect the Ship ports
    self.connectPorts(self.Canal_116_A.ship_out ,self.Confluence_107.ship_in[0])
    self.connectPorts(self.Dock_129.ship_out ,self.Canal_128_A.ship_in)
    self.connectPorts(self.Canal_128_B.ship_out ,self.Dock_129.ship_in)
    self.connectPorts(self.Lock_39.ship_out_high ,self.Canal_84_A.ship_in)
    self.connectPorts(self.Confluence_107.ship_out[0] ,self.Canal_116_B.ship_in)
    self.connectPorts(self.Canal_84_B.ship_out ,self.Lock_39.ship_in_high)
    self.connectPorts(self.Confluence_45.ship_out[0] ,self.Waterway_18_A.ship_in)
    self.connectPorts(self.Confluence_80.ship_out[0] ,self.Canal_84_B.ship_in)
    self.connectPorts(self.Canal_84_A.ship_out ,self.Confluence_80.ship_in[0])
    self.connectPorts(self.Waterway_110_A.ship_out ,self.Lock_39.ship_in_low)
    self.connectPorts(self.Canal_82_A.ship_out ,self.Confluence_80.ship_in[1])
    self.connectPorts(self.Lock_39.ship_out_low ,self.Waterway_110_B.ship_in)
    self.connectPorts(self.Confluence_80.ship_out[1] ,self.Canal_82_B.ship_in)
    self.connectPorts(self.Confluence_107.ship_out[1] ,self.Waterway_110_A.ship_in)
    self.connectPorts(self.Canal_81_A.ship_out ,self.Confluence_80.ship_in[2])
    self.connectPorts(self.Waterway_110_B.ship_out ,self.Confluence_107.ship_in[1])
    self.connectPorts(self.Waterway_29_A.ship_out ,self.Confluence_107.ship_in[2])
    self.connectPorts(self.Confluence_107.ship_out[2] ,self.Waterway_29_B.ship_in)
    self.connectPorts(self.Canal_125_A.ship_out ,self.Confluence_123.ship_in[0])
    self.connectPorts(self.Waterway_25_A.ship_out ,self.Confluence_45.ship_in[1])
    self.connectPorts(self.Confluence_123.ship_out[0] ,self.Canal_125_B.ship_in)
    self.connectPorts(self.Confluence_45.ship_out[1] ,self.Waterway_25_B.ship_in)
    self.connectPorts(self.Confluence_122.ship_out[0] ,self.Canal_125_A.ship_in)
    self.connectPorts(self.Waterway_17_A.ship_out ,self.Confluence_45.ship_in[2])
    self.connectPorts(self.Canal_125_B.ship_out ,self.Confluence_122.ship_in[0])
    self.connectPorts(self.Confluence_80.ship_out[2] ,self.Canal_81_B.ship_in)
    self.connectPorts(self.Anchorpoint_42.ship_out ,self.Waterway_17_A.ship_in)
    self.connectPorts(self.Canal_83_A.ship_out ,self.Confluence_80.ship_in[3])
    self.connectPorts(self.Generator_14.ship_out ,self.Anchorpoint_42.ship_in)
    self.connectPorts(self.Confluence_80.ship_out[3] ,self.Canal_83_B.ship_in)
    self.connectPorts(self.Confluence_80.ship_out[4] ,self.Canal_58_A.ship_in)
    self.connectPorts(self.Dock_100.ship_out ,self.Canal_83_A.ship_in)
    self.connectPorts(self.Lock_37.ship_out_low ,self.Waterway_30_A.ship_in)
    self.connectPorts(self.Canal_58_B.ship_out ,self.Confluence_80.ship_in[4])
    self.connectPorts(self.Waterway_30_B.ship_out ,self.Lock_37.ship_in_low)
    self.connectPorts(self.Dock_99.ship_out ,self.Canal_82_A.ship_in)
    self.connectPorts(self.Canal_127_A.ship_out ,self.Dock_130.ship_in)
    self.connectPorts(self.Canal_83_B.ship_out ,self.Dock_100.ship_in)
    self.connectPorts(self.Dock_130.ship_out ,self.Canal_127_B.ship_in)
    self.connectPorts(self.Dock_98.ship_out ,self.Canal_81_A.ship_in)
    self.connectPorts(self.Confluence_123.ship_out[1] ,self.Canal_128_B.ship_in)
    self.connectPorts(self.Canal_82_B.ship_out ,self.Dock_99.ship_in)
    self.connectPorts(self.Canal_128_A.ship_out ,self.Confluence_123.ship_in[1])
    self.connectPorts(self.Confluence_123.ship_out[2] ,self.Canal_127_A.ship_in)
    self.connectPorts(self.Canal_81_B.ship_out ,self.Dock_98.ship_in)
    self.connectPorts(self.Canal_127_B.ship_out ,self.Confluence_123.ship_in[2])
    self.connectPorts(self.Lock_38.ship_out_high ,self.Canal_124_A.ship_in)
    self.connectPorts(self.Waterway_29_B.ship_out ,self.Confluence_26.ship_in[0])
    self.connectPorts(self.Confluence_26.ship_out[0] ,self.Waterway_29_A.ship_in)
    self.connectPorts(self.Canal_58_A.ship_out ,self.Confluence_57.ship_in[0])
    self.connectPorts(self.Waterway_30_A.ship_out ,self.Confluence_26.ship_in[1])
    self.connectPorts(self.Confluence_57.ship_out[0] ,self.Canal_58_B.ship_in)
    self.connectPorts(self.Confluence_26.ship_out[1] ,self.Waterway_30_B.ship_in)
    self.connectPorts(self.Dock_61.ship_out ,self.Canal_59_A.ship_in)
    self.connectPorts(self.Canal_59_B.ship_out ,self.Dock_61.ship_in)
    self.connectPorts(self.Confluence_26.ship_out[2] ,self.Waterway_25_A.ship_in)
    self.connectPorts(self.Canal_59_A.ship_out ,self.Confluence_57.ship_in[1])
    self.connectPorts(self.Dock_131.ship_out ,self.Canal_126_A.ship_in)
    self.connectPorts(self.Confluence_57.ship_out[1] ,self.Canal_59_B.ship_in)
    self.connectPorts(self.Confluence_57.ship_out[2] ,self.Canal_56_A.ship_in)
    self.connectPorts(self.Canal_126_A.ship_out ,self.Confluence_122.ship_in[1])
    self.connectPorts(self.Canal_56_B.ship_out ,self.Confluence_57.ship_in[2])
    self.connectPorts(self.Canal_126_B.ship_out ,self.Dock_131.ship_in)
    self.connectPorts(self.Dock_60.ship_out ,self.Canal_55_A.ship_in)
    self.connectPorts(self.Confluence_122.ship_out[2] ,self.Canal_124_B.ship_in)
    self.connectPorts(self.Canal_55_B.ship_out ,self.Dock_60.ship_in)
    self.connectPorts(self.Confluence_122.ship_out[1] ,self.Canal_126_B.ship_in)
    self.connectPorts(self.Canal_124_B.ship_out ,self.Lock_38.ship_in_high)
    self.connectPorts(self.Canal_124_A.ship_out ,self.Confluence_122.ship_in[2])
    self.connectPorts(self.Waterway_25_B.ship_out ,self.Confluence_26.ship_in[2])
    self.connectPorts(self.Canal_116_B.ship_out ,self.Lock_38.ship_in_low)
    self.connectPorts(self.Lock_38.ship_out_low ,self.Canal_116_A.ship_in)
    self.connectPorts(self.Canal_56_A.ship_out ,self.Confluence_53.ship_in[0])
    self.connectPorts(self.Confluence_53.ship_out[0] ,self.Canal_56_B.ship_in)
    self.connectPorts(self.Canal_55_A.ship_out ,self.Confluence_53.ship_in[1])
    self.connectPorts(self.Confluence_53.ship_out[1] ,self.Canal_55_B.ship_in)
    self.connectPorts(self.Confluence_53.ship_out[2] ,self.Canal_54_A.ship_in)
    self.connectPorts(self.Waterway_18_A.ship_out ,self.Sea_4.ship_in)
    self.connectPorts(self.Canal_54_B.ship_out ,self.Confluence_53.ship_in[2])
    self.connectPorts(self.Canal_54_A.ship_out ,self.Lock_37.ship_in_high)
    self.connectPorts(self.Lock_37.ship_out_high ,self.Canal_54_B.ship_in)


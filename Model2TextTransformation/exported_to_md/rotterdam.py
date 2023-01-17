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
    self.Dock_174 = self.addSubModel(Dock(int("d4"[1:])))
    self.Dock_173 = self.addSubModel(Dock(int("d3"[1:])))
    self.Dock_172 = self.addSubModel(Dock(int("d2"[1:])))
    self.Dock_189 = self.addSubModel(Dock(int("d5"[1:])))
    self.Dock_220 = self.addSubModel(Dock(int("d7"[1:])))
    self.Dock_171 = self.addSubModel(Dock(int("d1"[1:])))
    self.Dock_219 = self.addSubModel(Dock(int("d8"[1:])))
    self.Dock_218 = self.addSubModel(Dock(int("d9"[1:])))
    self.Dock_190 = self.addSubModel(Dock(int("d6"[1:])))
    self.Dock_217 = self.addSubModel(Dock(int("d10"[1:])))

    # Locks
    # Also need to fix the naming here
    self.Lock_160 = self.addSubModel(Lock("Lock " + "LA"[-1]))

    # Need to convert these values to meters
    # Waterways (make 2 since they are only singly linked in our model)
    self.Waterway_17_A = self.addSubModel(Waterway("w_K_c1_A", 10.0*1000))
    self.Waterway_17_B = self.addSubModel(Waterway("w_K_c1_B", 10.0*1000))
    self.Waterway_18_A = self.addSubModel(Waterway("w_c1_S_A", 10.0*1000))
    self.Waterway_18_B = self.addSubModel(Waterway("w_c1_S_B", 10.0*1000))
    self.Waterway_25_A = self.addSubModel(Waterway("w_c1_CP_A", 6.85*1000))
    self.Waterway_25_B = self.addSubModel(Waterway("w_c1_CP_B", 6.85*1000))
    self.Waterway_187_A = self.addSubModel(Waterway("w_CP_c2_A", 9.8*1000))
    self.Waterway_187_B = self.addSubModel(Waterway("w_CP_c2_B", 9.8*1000))
      
    # Canal (make 2 since they are only singly linked in our model)
    self.Canal_199_A = self.addSubModel(Canal("c_C2_C3_A", 4.3*1000))
    self.Canal_199_B = self.addSubModel(Canal("c_C2_C3_B", 4.3*1000))
    self.Canal_163_A = self.addSubModel(Canal("c_LA_c1_A", 1.0*1000))
    self.Canal_163_B = self.addSubModel(Canal("c_LA_c1_B", 1.0*1000))
    self.Canal_206_A = self.addSubModel(Canal("c_d9_A", 1.4*1000))
    self.Canal_206_B = self.addSubModel(Canal("c_d9_B", 1.4*1000))
    self.Canal_207_A = self.addSubModel(Canal("c_d8_A", 1.6*1000))
    self.Canal_207_B = self.addSubModel(Canal("c_d8_B", 1.6*1000))
    self.Canal_208_A = self.addSubModel(Canal("c_d7_A", 1.0*1000))
    self.Canal_208_B = self.addSubModel(Canal("c_d7_B", 1.0*1000))
    self.Canal_205_A = self.addSubModel(Canal("c_d10_A", 1.2*1000))
    self.Canal_205_B = self.addSubModel(Canal("c_d10_B", 1.2*1000))
    
    self.Confluence_45 = self.addSubModel(CP("CP", 3+1, { 
0: 1, int("d4"[1:]):2, int("d3"[1:]):2, int("d2"[1:]):2, int("d5"[1:]):0, int("d7"[1:]):0, int("d1"[1:]):2, int("d8"[1:]):0, int("d9"[1:]):0, int("d6"[1:]):0, int("d10"[1:]):0, }))  # Note: this is a special case
    # Need to do some hacking here
    self.Confluence_164 = self.addSubModel(Confluence("c1", 5+1, {
0: 3, int("d4"[1:]):2, int("d3"[1:]):4, int("d2"[1:]):1, int("d5"[1:]):3, int("d7"[1:]):3, int("d1"[1:]):0, int("d8"[1:]):3, int("d9"[1:]):3, int("d6"[1:]):3, int("d10"[1:]):3, }))
    # Need to do some hacking here
    self.Confluence_188 = self.addSubModel(Confluence("c2", 4+1, {
0: 2, int("d4"[1:]):2, int("d3"[1:]):2, int("d2"[1:]):2, int("d5"[1:]):1, int("d7"[1:]):3, int("d1"[1:]):2, int("d8"[1:]):3, int("d9"[1:]):3, int("d6"[1:]):0, int("d10"[1:]):3, }))
    # Need to do some hacking here
    self.Confluence_202 = self.addSubModel(Confluence("c3", 5+1, {
0: 4, int("d4"[1:]):4, int("d3"[1:]):4, int("d2"[1:]):4, int("d5"[1:]):4, int("d7"[1:]):3, int("d1"[1:]):4, int("d8"[1:]):2, int("d9"[1:]):1, int("d6"[1:]):4, int("d10"[1:]):0, }))

    # Connect the PortDepartureRequests
    self.connectPorts(self.Dock_189.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_217.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_218.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_219.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_220.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_173.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_190.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_172.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_171.message_out ,self.ControlTower_3.message_in)
    self.connectPorts(self.Dock_174.message_out ,self.ControlTower_3.message_in)
    # Connect the PortEntryRequest
    self.connectPorts(self.Anchorpoint_42.message_out ,self.ControlTower_3.message_in)
    # Connect the PortEntryPermission
    self.connectPorts(self.ControlTower_3.message_out ,self.Anchorpoint_42.message_in)

    # Connect the Ship ports
    self.connectPorts(self.Confluence_188.ship_out[0] ,self.Dock_190.ship_in)
    self.connectPorts(self.Dock_190.ship_out ,self.Confluence_188.ship_in[0])
    self.connectPorts(self.Dock_189.ship_out ,self.Confluence_188.ship_in[1])
    self.connectPorts(self.Confluence_188.ship_out[1] ,self.Dock_189.ship_in)
    self.connectPorts(self.Waterway_187_A.ship_out ,self.Confluence_188.ship_in[2])
    self.connectPorts(self.Confluence_188.ship_out[2] ,self.Waterway_187_B.ship_in)
    self.connectPorts(self.Confluence_45.ship_out[0] ,self.Waterway_187_A.ship_in)
    self.connectPorts(self.Waterway_187_B.ship_out ,self.Confluence_45.ship_in[0])
    self.connectPorts(self.Confluence_45.ship_out[1] ,self.Waterway_18_A.ship_in)
    self.connectPorts(self.Waterway_25_A.ship_out ,self.Confluence_45.ship_in[2])
    self.connectPorts(self.Confluence_45.ship_out[2] ,self.Waterway_25_B.ship_in)
    self.connectPorts(self.Waterway_17_A.ship_out ,self.Confluence_45.ship_in[3])
    self.connectPorts(self.Dock_171.ship_out ,self.Confluence_164.ship_in[0])
    self.connectPorts(self.Anchorpoint_42.ship_out ,self.Waterway_17_A.ship_in)
    self.connectPorts(self.Dock_172.ship_out ,self.Confluence_164.ship_in[1])
    self.connectPorts(self.Generator_14.ship_out ,self.Anchorpoint_42.ship_in)
    self.connectPorts(self.Confluence_164.ship_out[0] ,self.Dock_171.ship_in)
    self.connectPorts(self.Canal_206_A.ship_out ,self.Dock_218.ship_in)
    self.connectPorts(self.Dock_218.ship_out ,self.Canal_206_B.ship_in)
    self.connectPorts(self.Canal_207_A.ship_out ,self.Dock_219.ship_in)
    self.connectPorts(self.Dock_219.ship_out ,self.Canal_207_B.ship_in)
    self.connectPorts(self.Canal_208_A.ship_out ,self.Dock_220.ship_in)
    self.connectPorts(self.Dock_220.ship_out ,self.Canal_208_B.ship_in)
    self.connectPorts(self.Canal_205_A.ship_out ,self.Dock_217.ship_in)
    self.connectPorts(self.Dock_217.ship_out ,self.Canal_205_B.ship_in)
    self.connectPorts(self.Confluence_164.ship_out[2] ,self.Dock_174.ship_in)
    self.connectPorts(self.Dock_174.ship_out ,self.Confluence_164.ship_in[2])
    self.connectPorts(self.Confluence_164.ship_out[3] ,self.Canal_163_A.ship_in)
    self.connectPorts(self.Canal_205_B.ship_out ,self.Confluence_202.ship_in[0])
    self.connectPorts(self.Canal_206_B.ship_out ,self.Confluence_202.ship_in[1])
    self.connectPorts(self.Confluence_202.ship_out[0] ,self.Canal_205_A.ship_in)
    self.connectPorts(self.Confluence_164.ship_out[1] ,self.Dock_172.ship_in)
    self.connectPorts(self.Canal_207_B.ship_out ,self.Confluence_202.ship_in[2])
    self.connectPorts(self.Confluence_202.ship_out[1] ,self.Canal_206_A.ship_in)
    self.connectPorts(self.Confluence_164.ship_out[4] ,self.Dock_173.ship_in)
    self.connectPorts(self.Confluence_202.ship_out[3] ,self.Canal_208_A.ship_in)
    self.connectPorts(self.Dock_173.ship_out ,self.Confluence_164.ship_in[4])
    self.connectPorts(self.Confluence_202.ship_out[2] ,self.Canal_207_A.ship_in)
    self.connectPorts(self.Canal_208_B.ship_out ,self.Confluence_202.ship_in[3])
    self.connectPorts(self.Lock_160.ship_out_low ,self.Waterway_25_A.ship_in)
    self.connectPorts(self.Waterway_25_B.ship_out ,self.Lock_160.ship_in_low)
    self.connectPorts(self.Waterway_18_A.ship_out ,self.Sea_4.ship_in)
    self.connectPorts(self.Canal_199_A.ship_out ,self.Confluence_202.ship_in[4])
    self.connectPorts(self.Confluence_202.ship_out[4] ,self.Canal_199_B.ship_in)
    self.connectPorts(self.Canal_199_B.ship_out ,self.Confluence_188.ship_in[3])
    self.connectPorts(self.Canal_163_B.ship_out ,self.Confluence_164.ship_in[3])
    self.connectPorts(self.Lock_160.ship_out_high ,self.Canal_163_B.ship_in)
    self.connectPorts(self.Canal_163_A.ship_out ,self.Lock_160.ship_in_high)
    self.connectPorts(self.Confluence_188.ship_out[3] ,self.Canal_199_A.ship_in)


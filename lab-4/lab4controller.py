# Lab 4 controller skeleton 
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet
    if packet.type == packet.ARP_TYPE:
      print("ARP Packet")
      accept()
    elif packet.type == packet.ICMP_TYPE:
      print("ICMP Packet")
      accept()

    def accept():
      #allow all ARP and ICMP traffic across the network
      # Write code for an accept function

      # ARP
    
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(msg)

      

      print("Packet Accepted - Flow Table Installed on Switches")

    def drop():
      # Write code for a drop function
      # Drop packet
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      self.connection.send(msg)
      print("Packet Dropped - Flow Table Installed on Switches")

    # Write firewall code 
    print("Example Code")

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the components
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
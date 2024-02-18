# Lab 4 controller skeleton
#
# # Based on of_tutorial by James McCauley
# General Connectivity: Allow all ARP and ICMP traffic across the network to facilitate general
# network connectivity.
# 2. Web Traffic: Allow all TCP traffic between workstations (WS) or personal computers (PC) within
# the University (not from the internet) and the web server (webServer).
# 3. Faculty Access: Allow all TCP traffic between faculty WS and PC with the exam server
# (examServer).
# 4. IT Management: Allow all TCP and UDP traffic between IT WS and PC with any WS or PC
# within the University (not from the internet).
# 5. DNS Traffic: Allow all UDP traffic between WSs or PCs within the University (not from the
# internet) and the DNS server (dnsServer).
# 6. Default Deny: Block all traffic that does not match the above criteria.

import pox.openflow.libopenflow_01 as of
from pox.core import core

ips = {
    "facultyWS": "10.0.0.2",
    "facultyPC": "10.0.0.4",
    "printer": "10.0.1.3",
    "studentPC": "10.0.2.2",
    "labWS": "10.0.2.3",
    "itWS": "10.0.3.2",
    "itPC": "10.0.3.3",
    "examServer": "10.0.100.2",
    "webServer": "10.0.100.3",
    "dnsServer": "10.0.100.4",
    "trustedPC": "10.0.203.2",
    "guestPC": "10.0.198.2",
}
table_rule= [
    [None, None, None, None, ["ARP"], True],#1
    [None, None, None, None, ["ICMP", "UDP"], True],#2
    [ ["facultyWS", "facultyPC", "labWS", "studentPC", "itWS", "itPC"], None, ["webServer"], None, ["TCP", "UDP"], True,],#3
    [ ["webServer"], None, ["facultyWS", "facultyPC", "labWS", "studentPC", "itWS", "itPC"], None, ["TCP"], True,],#4
    [ ["facultyWS", "facultyPC"], None, ["examServer"], None, ["TCP"], True,],#5
    [ ["examServer"], None, ["facultyWS", "facultyPC"],  None, ["TCP"], True,],#6
    [ ["itWS", "itPC"], None, ["facultyWS", "facultyPC", "studentPC", "labWS", "itWS", "itPC"], None, ["TCP", "UDP"], True,],#7
    [ ["facultyWS", "facultyPC", "labWS", "itWS", "itPC", "studentPC"], None, ["itWS", "itPC"], None, ["TCP", "UDP"], True,],#8
    [ ["facultyWS", "facultyPC", "labWS", "itWS", "itPC", "studentPC"], None, ["dnsServer"], None, ["UDP"], True,],#9
    [ ["dnsServer"], None, ["facultyWS", "facultyPC", "labWS", "itWS", "itPC", "studentPC"], None, ["UDP"], True,],#10
    [None, None, None, None, None, False],#11
]


log = core.getLogger()
dc_class_c = 100
IT_class_c = 3
SH_class_c = 2
faculty_class_c = 1

split_ip = ip.split(".")  # returns an array of [10, 0, 100, 2]
if len(split_ip) != 4:  # or the first octet is not 10 or the second is not 0
    # throw some error, this was not a valid ipv4
    pass
else:
    # it is a valid ipv4
    if split_ip[2] == dc_class_c:
        # if you are here, this is a data center ip
        pass


class Firewall(object):
    """
    A Firewall object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """

    def __init__(self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)

    def do_firewall(self, packet, packet_in):
        # The code in here will be executed for every packet
        ip = packet.find("ipv4")
        if ip is not None:
            src = ip.srcip
        if src == None:
            print("No source IP")
        dst = ip.dstip
        if dst == None:
            print("No destination IP")
        else:
            print("No IP header found")
        tcp = packet.find("tcp")
        if tcp == None:
            print("No tcp")
        icmp = packet.find("icmp")
        if icmp == None:
            print("No icmp")
        udp = packet.find("udp")
        if udp == None:
            print("No udp")
        arp = packet.find("arp")
        if arp == None:
            print("No arp")

        def accept():
            table = of.ofp_flow_mod()
            table.match = of.ofp_match.from_packet(packet)
            table.idle_timeout = 30
            table.hard_timeout = 30
            table.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            table.buffer_id = packet_in.buffer_id
            self.connection.send(table)

            print("Packet Accepted - Flow Table Installed on Switches")

        def drop():
            # Write code for a drop function
            # Drop packet
            table = of.ofp_flow_mod()
            table.match = of.ofp_match.from_packet(packet)
            table.idle_timeout = 30
            table.hard_timeout = 30
            table.buffer_id = packet_in.buffer_id
            self.connection.send(table)
            print("Packet Dropped - Flow Table Installed on Switches")

            # Write firewall code
        def check_rule(src_ip, dest_ip, protocol):
          for i in range(len(table_rule)):
              if protocol in table_rule[i][4]:
                  if (
                      (table_rule[i][0] is None and table_rule[i][1] is None)
                      or (
                          table_rule[i][0] is not None
                          and src_ip in [ips[host] for host in table_rule[i][0]]
                      )
                      or (table_rule[i][1] is not None and src_ip in table_rule[i][1])
                  ):
                      if (
                          (table_rule[i][2] is None and table_rule[i][3] is None)
                          or (
                              table_rule[i][2] is not None
                              and dest_ip in [ips[host] for host in table_rule[i][2]]
                          )
                          or (table_rule[i][3] is not None and dest_ip in table_rule[i][3])
                      ):
                          return table_rule[i][5]
          return False
        if ip is not None:
            src_ip = ip.srcip
            dest_ip = ip.dstip
            protocol = ip.protocol
            if check_rule(src_ip, dest_ip, protocol) == True:
                accept()
            else:
                drop() 


            

    def _handle_PacketIn(self, event):
        """
        Handles packet in messages from the switch.
        """

        packet = event.parsed  # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp  # The actual ofp_packet_in message.
        self.do_firewall(packet, packet_in)


def launch():
    """
    Starts the components
    """

    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Firewall(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

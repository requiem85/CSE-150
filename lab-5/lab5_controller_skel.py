## Lab5 Skeleton
"""   
    self.addLink(FacultyLan, CoreSwitch, port1=10, port2=10)
    self.addLink(StudentLan, CoreSwitch, port1=20 , port2=20)
    self.addLink(ItLan, CoreSwitch, port1=30, port2=30)
    self.addLink(DataCenter, CoreSwitch, port1=100, port2=100)
    self.addLink(facutlyWS, FacultyLan, port1=11, port2=41)
    self.addLink(printer, FacultyLan, port1=12, port2=42)
    self.addLink(facultyPC, FacultyLan, port1=13, port2=43)
    self.addLink(studentPC, StudentLan, port1=21, port2=51)
    self.addLink(labWS, StudentLan, port1=22, port2=52)
    self.addLink(itWS, ItLan, port1=31, port2=61)
    self.addLink(itPC, ItLan, port1=32, port2=62)
    self.addLink(examServer, DataCenter, port1=101, port2=401)
    self.addLink(webServer, DataCenter, port1=102, port2=402)
    self.addLink(dnsServer, DataCenter, port1=103, port2=403)
    self.addLink(trustedPC, CoreSwitch, port1=200, port2=200)
    self.addLink(guestPC, CoreSwitch, port1=201, port2=201)"""


from pox.core import core

import pox.openflow.libopenflow_01 as of

log = core.getLogger()

ips = {
    "facultyWS": "10.0.1.2",
    "facultyPC": "10.0.1.4",
    "printer": "10.0.1.3",
    "studentPC": "10.0.2.2",
    "labWS": "10.0.2.3",
    "itWS": "10.0.3.2",
    "itPC": "10.0.3.3",
    "examServer": "10.0.100.2",
    "webServer": "10.0.100.3",
    "dnsServer": "10.0.100.4",
    "trustedPC": "200.20.203.2",
    "guestPC": "200.20.198.2",
}


# switchboard = [
#     [["10.0.1.2", "10.0.1.4", "10.0.1.3"], [10], ["ICMP", "TCP", "UDP"], True],
#     [["10.0.2.2", "10.0.2.3"], [20], ["ICMP", "TCP", "UDP"], False],
#     [["10.0.3.2", "10.0.3.3"], [30], ["ICMP", "TCP", "UDP"], False],
#     [["10.0.100.2", "10.0.100.3", "10.0.100.4"], [100], ["TCP", "UDP"], False],
#     [["10.0.203.2"], [200], ["TCP", "same"], False],
#     [["10.0.198.2"], [201], ["same"], False],
# ]

switchboard = [
    [
        # switch_id, subnet, port, allowed protocols
        [1, 1, 1, ["ICMP", "TCP", "UDP"]],
        [2, 2, 2, ["ICMP", "TCP", "UDP"]],
        [3, 3, 3, ["ICMP", "TCP", "UDP"]],
        [4, 100, 4, ["TCP", "UDP"]],
        # [200, 203, 99, ["TCP"]],
    ],
    # ip, dst_port, switch_port
    [
        ("10.0.1.2", 11, 41),
        ("10.0.1.3", 12, 42),
        ("10.0.1.4", 13, 43),
    ],
    [
        ("10.0.2.2", 21, 51),
        ("10.0.2.3", 22, 52),
    ],
    [
        ("10.0.3.2", 31, 61),
        ("10.0.3.3", 32, 62),
    ],
    [
        ("10.0.100.2", 17, 18),
        ("10.0.100.3", 102, 402),
        ("10.0.100.4", 105, 403),
        # ("200.20.203.2", 99, 200),
        # ("200.20.198.2", 98, 201),
    ],
]

internet = {
    "200.20.203.2": [1, 2, 3, 100],
    "200.20.198.2": [],
    "200.20.50.5": [2]
}

escape_ports = {
    "10.0.1.2": (11, 41),
    "10.0.1.3": (12, 42),
    "10.0.1.4": (13, 43),
    "10.0.2.2": (21, 51),
    "10.0.2.3": (22, 52),
    "10.0.3.2": (31, 61),
    "10.0.3.3": (32, 62),
    "10.0.100.2": (17, 18),
    "10.0.100.3": (102, 402),
    "10.0.100.4": (105, 403),
    "200.20.203.2": (99, 200),
    "200.20.198.2": (98, 201),
    "200.20.50.5": (123, 321)
}


class Routing(object):

    def __init__(self, connection):
        # Keep track of the connection to the switch so that we can
        # send it messages!
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)

    def do_routing(self, packet, packet_in, port_on_switch, switch_id):
        # port_on_swtich - the port on which this packet was received
        # switch_id - the switch which received this packet

        # Your code here
        print(switch_id)
        print("-------")
        print(port_on_switch)
        print("-------")

        # end_port = 0

        def accept(end_port):
            print("accept port", end_port)
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 45
            msg.hard_timeout = 45
            if packet is not None:
                log.debug(packet)
            msg.actions.append(of.ofp_action_output(port=end_port))
            msg.buffer_id = packet_in.buffer_id
            msg.data = packet_in
            self.connection.send(msg)
            print("Packet Accepted - Flow Table Installed on Switches")

        def drop():
            # Write code for a drop function
            # Drop packet
            print("bye")
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 30
            msg.buffer_id = packet_in.buffer_id
            self.connection.send(msg)
            print("Packet Dropped - Flow Table Installed on Switches")

        def checkrule(ip, sw, protocol):
            src = str(ip.srcip)
            dst = str(ip.dstip)
            # print("Source:", ip.srcip)
            # print("Source:", src)
            # # print("Dest:", ip.dstip)
            # print("Dest:", dst)

            # Write firewall code
            # Check if switch_id is not None
            if sw is not None:
                # print("Switch:", sw)
                # Check if destination IP is in the switchboard table
                src_subnet = int(src.split(".")[2])
                dst_subnet = int(dst.split(".")[2])

                if sw not in [1, 2, 3, 4]:
                    print("Navigating via coreswitch")
                    if dst in internet:
                        print("The internet!")
                        if src_subnet in internet[dst]:
                            _, end_port = escape_ports[dst]
                            accept(end_port)
                        else:
                            drop()
                    else:
                        print("the university")
                        for row in switchboard[0]:
                            if dst_subnet == row[1] and protocol in row[3]:
                                end_port = row[2]
                                accept(end_port)
                                print("End port", end_port)
                                return
                                # sw = None
                        # if sw == None:
                        drop()
                else:
                    print("Navigating within switch", sw)
                    if dst_subnet == switchboard[0][sw - 1][1]:
                        print("Destination is in same switch")
                        # for t in switchboard[sw]:
                        #     tmp_ip, _, tmp_port = t
                        #     if tmp_ip == ip.dstip:
                        #         end_port = tmp_port
                        #         accept()
                        #         return
                        # drop()
                        if dst in escape_ports and (dst != "10.0.100.2" or src_subnet == 1):
                            _, end_port = escape_ports[dst]
                            accept(end_port)
                        else:
                            drop()
                    else:
                        print("Destination is in different switch")
                        # if protocol in switchboard[0][sw - 1][3]:
                        end_port = switchboard[0][sw - 1][2]
                        accept(end_port)
                      
            else:
                drop()
            # print("End port", end_port)
            return

           

        icmp = packet.find("icmp")
        tcp = packet.find("tcp")
        udp = packet.find("udp")
        protocol = None

        if icmp:
            protocol = "ICMP"
        elif tcp:
            protocol = "TCP"
        elif udp:
            protocol = "UDP"
        else:
            print("drop_else")
            drop()
            return

        ip = packet.find("ipv4")
        print(packet_in)
        if ip is not None:
            print(ip, ip.protocol)

            # accept(15)
            checkrule(ip, switch_id, protocol)
            # accept()
        else:
            drop()
        return

   
    def _handle_PacketIn(self, event):
        """
        Handles packet in messages from the switch.
        """
        packet = event.parsed  # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        print(packet)
        print(event.dpid)
        packet_in = event.ofp  # The actual ofp_packet_in message.
        self.do_routing(packet, packet_in, event.port, event.dpid)


def launch():
    """
    Starts the component
    """

    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Routing(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

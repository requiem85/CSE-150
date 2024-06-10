
#commands to run code
#rm ~/pox/pox/misc/lab5_controller_skel.py
#cp lab5_controller_skel.py ~/pox/pox/misc/
#sudo ~/pox/pox.py log.level --packet=WARN misc.lab5_controller_skel
from pox.core import core

import pox.openflow.libopenflow_01 as of
import time

log = core.getLogger()

ips = {
    "h101": "128.114.1.101",
    "h102": "128.114.1.102",
    "h103": "128.114.1.103",
    "h104": "128.114.1.104",
    "h201": "128.114.2.201",
    "h202": "128.114.2.202",
    "h203": "128.114.2.203",
    "h204": "128.114.2.204",
    "h_server": "128.114.3.178",
    "h_trust": "200.20.203.2",
    "h_untrust": "108.35.24.113",
}

switchboard = [
    [
        # switch_id, subnet, port, allowed protocols
        [1, 1, 1, ["ICMP", "TCP", "UDP"]], # floor 1 switch 1
        [2, 1, 2, ["ICMP", "TCP", "UDP"]], # floor 1 switch 2
        [3, 2, 3, ["ICMP", "TCP", "UDP"]], # floor 2 switch 1
        [4, 2, 4, ["ICMP", "TCP", "UDP"]], # floor 2 switch 2
        [5, 3, 5, ["ICMP", "TCP", "UDP"]], # datacenter
        #[4, 100, 4, ["TCP", "UDP"]],
        # [200, 203, 99, ["TCP"]],
    ],
    # ip, dst_port, switch_port
    {
        ips["h101"]: (11, 41),
        ips["h102"]: (12, 42),
        
    },
    {
        ips["h103"]: (13, 43),
        ips["h104"]: (14, 44),

    },
    {
        ips["h201"]: (21, 51),
        ips["h202"]: (22, 52),
    },
    {
        ips["h203"]: (23, 53),
        ips["h204"]: (24, 54),
        

    },
    {
        ips["h_server"]: (17, 18),
        
    },
]

internet = {
    ips["h_trust"]: [1, 2, 3, 4, 5, 6], # which subnet(s) h_trust is allowed to ping
    ips["h_untrust"]: [1, 2, 3, 4, 5, 6],   
    
}

allowed_connections = {
    1: [1, 2, 3, 4, 5, 6], # subnet 1 is allowed to connect to subnets 1 and 3
    2: [1, 2, 3, 4, 5, 6],
    3: [1, 2, 3, 4, 5, 6],
}

escape_ports = {
    ips["h101"]: (11, 41),
    ips["h102"]: (12, 42),
    ips["h103"]: (13, 43),
    ips["h104"]: (14, 44),
    ips["h201"]: (21, 51),
    ips["h202"]: (22, 52),
    ips["h203"]: (23, 53),
    ips["h204"]: (24, 54),
    ips["h_server"]: (17, 18),
    ips["h_trust"]: (99, 200),
    ips["h_untrust"]: (98, 201),
    # "200.20.50.5": (123, 321)
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
            print("Source:", ip.srcip)
            print("Source:", src)
            print("Dest:", ip.dstip)
            print("Dest:", dst)

            # Write firewall code
            # Check if switch_id is not None
            if sw is not None:
                print("Switch:", sw)
                # Check if destination IP is in the switchboard table
                src_subnet = int(src.split(".")[2])
                dst_subnet = int(dst.split(".")[2])

                if sw not in [1, 2, 3, 4, 5]:
                    print("Navigating via coreswitch")
                    print(src, dst, src_subnet, dst_subnet)
                    # time.sleep(10)
                    if dst in internet:
                        print("The internet!")
                        if src_subnet in internet[dst]:
                            _, end_port = escape_ports[dst]
                            accept(end_port)
                        else:
                            drop()
                    else:
                        print("the company network!")
                        if dst_subnet not in allowed_connections[src_subnet]:
                            drop()
                        else:
                            for row in switchboard[0]:
                                if dst_subnet == row[1] and protocol in row[3] and dst in switchboard[row[0]]:
                                    end_port = row[2]
                                    accept(end_port)
                                    print("End port", end_port)
                                    return
                                    # sw = None
                            # if sw == None:
                            drop()
                else:
                    print("Navigating within switch", sw)
                    # if dst_subnet == switchboard[0][sw - 1][1]:
                    if dst in switchboard[sw]:
                        print("Destination is in same switch")
                        # for t in switchboard[sw]:
                        #     tmp_ip, _, tmp_port = t
                        #     if tmp_ip == ip.dstip:
                        #         end_port = tmp_port
                        #         accept()
                        #         return
                        # drop()
                        if dst in escape_ports:# and (dst != "10.0.100.2" or src_subnet == 1):
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

        print('packet', packet)
        print('dpid', event.dpid)
        packet_in = event.ofp  # The actual ofp_packet_in message.
        print('packet_in', packet_in)
        print('event.port', event.port)
        self.do_routing(packet, packet_in, event.port, event.dpid)


def launch():
    """
    Starts the component
    """

    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Routing(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Define the IPs of the hosts
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
    "h_trust": "192.47.38.109",
    "h_untrust": "108.35.24.113",
    "discord": "200.20.50.5"
}

# Define the switchboard (configuration for routing)
switchboard = {
    1: {"subnet": 1, "ports": {41: "128.114.1.101", 42: "128.114.1.102"}},
    2: {"subnet": 2, "ports": {51: "128.114.2.201", 52: "128.114.2.202"}},
    3: {"subnet": 3, "ports": {61: "128.114.2.203", 62: "128.114.2.204"}},
    4: {"subnet": 100, "ports": {18: "128.114.3.178"}},
    0: {"subnet": None, "ports": {321: "200.20.50.5"}}
}

internet = {
    "192.47.38.109": [1, 2, 3, 100],  # Trusted host access to all subnets
    "108.35.24.113": []  # Untrusted host access
}

escape_ports = {
    "128.114.1.101": (41, 1),
    "128.114.1.102": (42, 1),
    "128.114.1.103": (43, 1),
    "128.114.1.104": (44, 1),
    "128.114.2.201": (51, 2),
    "128.114.2.202": (52, 2),
    "128.114.2.203": (53, 2),
    "128.114.2.204": (54, 2),
    "128.114.3.178": (18, 4),
    "192.47.38.109": (200, 3),
    "108.35.24.113": (201, 0),
    "200.20.50.5": (321, 0)
}

class Routing(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def do_routing(self, packet, packet_in, port_on_switch, switch_id):
        def accept(end_port):
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 45
            msg.hard_timeout = 45
            msg.actions.append(of.ofp_action_output(port=end_port))
            msg.buffer_id = packet_in.buffer_id
            msg.data = packet_in
            self.connection.send(msg)
            log.debug("Packet Accepted - Flow Table Installed on Switches")

        def drop():
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 30
            msg.buffer_id = packet_in.buffer_id
            self.connection.send(msg)
            log.debug("Packet Dropped - Flow Table Installed on Switches")

        def checkrule(ip, sw, protocol):
            src = str(ip.srcip)
            dst = str(ip.dstip)

            if sw is not None:
                src_subnet = int(src.split(".")[2])
                dst_subnet = int(dst.split(".")[2])

                if sw not in switchboard:
                    log.debug("Navigating via core switch")
                    if dst in internet:
                        if src_subnet in internet[dst]:
                            end_port, _ = escape_ports[dst]
                            accept(end_port)
                        else:
                            drop()
                    else:
                        log.debug("Navigating within the university")
                        for row in switchboard.values():
                            if dst_subnet == row["subnet"] and protocol in ["ICMP", "TCP", "UDP"]:
                                for port, ip in row["ports"].items():
                                    if ip == dst:
                                        accept(port)
                                        return
                        drop()
                else:
                    log.debug(f"Navigating within switch {sw}")
                    if dst_subnet == switchboard[sw]["subnet"]:
                        if dst in escape_ports:
                            end_port, _ = escape_ports[dst]
                            accept(end_port)
                        else:
                            drop()
                    else:
                        end_port, _ = switchboard[sw]["ports"].items()[0]
                        accept(end_port)
            else:
                drop()

        icmp = packet.find("icmp")
        tcp = packet.find("tcp")
        udp = packet.find("udp")
        protocol = "ICMP" if icmp else "TCP" if tcp else "UDP" if udp else None

        if not protocol:
            drop()
            return

        ip = packet.find("ipv4")
        if ip:
            checkrule(ip, switch_id, protocol)
        else:
            drop()

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp
        self.do_routing(packet, packet_in, event.port, event.dpid)

def launch():
    def start_switch(event):
        log.debug("Controlling %s" % (event.connection,))
        Routing(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

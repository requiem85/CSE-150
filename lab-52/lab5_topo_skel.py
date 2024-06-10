#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController


# ips = {
#     "h101": "128.114.1.101",
#     "h102": "128.114.1.102",
#     "h103": "128.114.1.103",
#     "h104": "128.114.1.104",
#     "h201": "128.114.2.201",
#     "h202": "128.114.2.202",
#     "h203": "128.114.2.203",
#     "h204": "128.114.2.204",
#     "h_server": "128.114.3.178",
#     "h_trust": "200.20.203.2",
#     "h_untrust": "108.35.24.113",
# }

# switchboard = [
#     [
#         # switch_id, subnet, port, allowed protocols
#         [1, 1, 1, ["ICMP", "TCP", "UDP"]],
#         [2, 2, 2, ["ICMP", "TCP", "UDP"]],
#         [3, 3, 3, ["ICMP", "TCP", "UDP"]],
#         [4, 100, 4, ["TCP", "UDP"]],
#         # [200, 203, 99, ["TCP"]],
#     ],
#     # ip, dst_port, switch_port
#     [
#         (ips["h101"], 11, 41),
#         (ips["h102"], 12, 42),
#         (ips["h103"], 13, 43),
#     ],
#     [
#         (ips["h201"], 21, 51),
#         (ips["h202"], 22, 52),
#     ],
#     [
#         (ips["h203"], 31, 61),
#         (ips["h204"], 32, 62),
#     ],
#     [
#         (ips["h_server"], 17, 18),
        
#     ],
# ]

# internet = {
#     ips["h_trust"]: [1, 2, 3, 100],
#     ips["h_untrust"]: [],
    
# }

# escape_ports = {
#     ips["h101"]: (11, 41),
#     ips["h102"]: (12, 42),
#     ips["h103"]: (13, 43),
#     ips["h201"]: (21, 51),
#     ips["h202"]: (22, 52),
#     ips["h203"]: (31, 61),
#     ips["h204"]: (32, 62),
#     ips["h_server"]: (17, 18),
#     ips["h_server"]: (102, 402),
#     ips["h_server"]: (105, 403),
#     ips["h_trust"]: (99, 200),
#     ips["h_untrust"]: (98, 201),
#     "200.20.50.5": (123, 321)
# }


class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)
    CoreSwitch = self.addSwitch('s0')
    Floor1Switch1 = self.addSwitch('s1')
    Floor2Switch1 = self.addSwitch('s2')
    TrustedSwitch = self.addSwitch('s3')
    DataCenterSwitch = self.addSwitch('s4')
    Floor1Switch2 = self.addSwitch('s5')
    Floor2Switch2 = self.addSwitch('s6')
    
    self.addLink(Floor1Switch1, CoreSwitch, port1=1, port2=1)
    self.addLink(Floor2Switch1, CoreSwitch, port1=2, port2=2)
    self.addLink(Floor1Switch2, CoreSwitch, port1=3, port2=3)
    self.addLink(Floor2Switch2, CoreSwitch, port1=4, port2=4)
    self.addLink(TrustedSwitch, CoreSwitch, port1=5, port2=5)
    self.addLink(DataCenterSwitch, CoreSwitch, port1=6, port2=6)
    
    # Floor 1 Hosts
    h101 = self.addHost('h101', ip='128.114.1.101/24', defaultRoute="h101-eth0", mac='00:00:00:00:00:01')
    self.addLink(h101, Floor1Switch1, port1=11, port2=41)
    h102 = self.addHost('h102', ip='128.114.1.102/24', defaultRoute="h102-eth0", mac='00:00:00:00:00:02')
    self.addLink(h102, Floor1Switch1, port1=12, port2=42)
    h103 = self.addHost('h103', ip='128.114.1.103/24', defaultRoute="h103-eth0", mac='00:00:00:00:00:03')
    self.addLink(h103, Floor1Switch2, port1=13, port2=43)
    h104 = self.addHost('h104', ip='128.114.1.104/24', defaultRoute="h104-eth0", mac='00:00:00:00:00:04')
    self.addLink(h104, Floor1Switch2, port1=14, port2=44)

    # Floor 2 Hosts
    h201 = self.addHost('h201', ip='128.114.2.201/24', defaultRoute="h201-eth0", mac='00:00:00:00:00:05')
    self.addLink(h201, Floor2Switch1, port1=21, port2=51)
    h202 = self.addHost('h202', ip='128.114.2.202/24', defaultRoute="h202-eth0", mac='00:00:00:00:00:06')
    self.addLink(h202, Floor2Switch1, port1=22, port2=52)
    h203 = self.addHost('h203', ip='128.114.2.203/24', defaultRoute="h203-eth0", mac='00:00:00:00:00:07')
    self.addLink(h203, Floor2Switch2, port1=23, port2=53)
    h204 = self.addHost('h204', ip='128.114.2.204/24', defaultRoute="h204-eth0", mac='00:00:00:00:00:08')
    self.addLink(h204, Floor2Switch2, port1=24, port2=54)

    # Trusted Host
    h_trust = self.addHost('h_trust', ip='192.47.38.109/24', defaultRoute="h_trust-eth0", mac='00:00:00:00:00:09')
    self.addLink(h_trust, TrustedSwitch, port1=99, port2=200)

    # Untrusted Host
    h_untrust = self.addHost('h_untrust', ip='108.35.24.113/24', defaultRoute="h_untrust-eth0", mac='00:00:00:00:00:10')
    self.addLink(h_untrust, CoreSwitch, port1=98, port2=201)
    
    # LLM Server
    h_server = self.addHost('h_server', ip='128.114.3.178/24', defaultRoute="h_server-eth0", mac='00:00:00:00:00:11')
    self.addLink(h_server, DataCenterSwitch, port1=17, port2=18)

    discord = self.addHost('discord', ip='200.20.50.5/32', defaultRoute="discord-eth0", mac="00:00:00:00:00:ff")
    self.addLink(discord, CoreSwitch, port1=123, port2=321)

if __name__ == '__main__':
  # This part of the script is run when the script is executed
  topo = MyTopology() # Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) # Creates a remote controller
  net = Mininet(topo=topo, controller=c0) # Loads the topology
  net.start() # Starts mininet
  net.staticArp()
  CLI(net) # Opens a command line to run commands on the simulated topology
  net.stop() # Stops mininet

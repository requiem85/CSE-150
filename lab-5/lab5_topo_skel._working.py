#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)
    CoreSwitch = self.addSwitch('s0')
    FacultyLan = self.addSwitch('s1')
    StudentLan = self.addSwitch('s2')
    ItLan = self.addSwitch('s3')
    DataCenter = self.addSwitch('s4')
    self.addLink(FacultyLan, CoreSwitch, port1=1, port2=1)
    self.addLink(StudentLan, CoreSwitch, port1=2 , port2=2)
    self.addLink(ItLan, CoreSwitch, port1=3, port2=3)
    self.addLink(DataCenter, CoreSwitch, port1=4, port2=4)
    
         
    facutlyWS = self.addHost('facultyWS', ip='10.0.1.2/24', defaultRoute="facultyWS-eth11", mac='00:00:00:00:00:01')
    self.addLink(facutlyWS, FacultyLan, port1=11, port2=41)
    printer = self.addHost('printer', ip='10.0.1.3/24', defaultRoute="printer-eth12", mac='00:00:00:00:00:02')
    self.addLink(printer, FacultyLan, port1=12, port2=42)
    facultyPC = self.addHost('facultyPC', ip='10.0.1.4/24', defaultRoute="facultyPC-eth13", mac='00:00:00:00:00:03')
    self.addLink(facultyPC, FacultyLan, port1=13, port2=43)


    studentPC = self.addHost('studentPC', ip='10.0.2.2/24', defaultRoute="studentPC-eth21", mac='00:00:00:00:00:04')
    self.addLink(studentPC, StudentLan, port1=21, port2=51)
    labWS = self.addHost('labWS', ip='10.0.2.3/24', defaultRoute="labWS-eth22", mac='00:00:00:00:00:05')
    self.addLink(labWS, StudentLan, port1=22, port2=52)


    itWS = self.addHost('itWS', ip='10.0.3.2/24', defaultRoute="itWS-eth31", mac='00:00:00:00:00:06')
    self.addLink(itWS, ItLan, port1=31, port2=61)
    itPC = self.addHost('itPC', ip='10.0.3.3/24', defaultRoute="itPC-eth32", mac='00:00:00:00:00:07')
    self.addLink(itPC, ItLan, port1=32, port2=62)


    examServer = self.addHost('exam', ip='10.0.100.2/24', defaultRoute="exam-eth17", mac='00:00:00:00:01:06')
    self.addLink(examServer, DataCenter, port1=17, port2=18)
    webServer = self.addHost('web', ip='10.0.100.3/24', defaultRoute="web-eth102", mac='00:00:00:00:00:09')
    self.addLink(webServer, DataCenter, port1=102, port2=402)
    dnsServer = self.addHost('dns', ip='10.0.100.4/24', defaultRoute='dns-eth105', mac='00:00:00:00:00:10')
    self.addLink(dnsServer, DataCenter, port1=105, port2=403)
   
    trustedPC = self.addHost('trusted', ip='200.20.203.2/32', defaultRoute="trusted-eth99", mac='00:00:00:00:00:11')
    self.addLink(trustedPC, CoreSwitch, port1=99, port2=200)
    guestPC = self.addHost('guest', ip='200.20.198.2/32', defaultRoute="guest-eth98", mac='00:00:00:00:00:12')
    self.addLink(guestPC, CoreSwitch, port1=98, port2=201)
    
    discord = self.addHost('discord', ip='200.20.50.5/32', defaultRoute="discord-eth123", mac="00:00:00:00:00:ff")
    self.addLink(discord, CoreSwitch, port1=123, port2=321)
    

if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  net.staticArp()
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
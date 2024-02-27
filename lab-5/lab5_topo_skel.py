#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)
    FacultyLan = self.addSwitch('s1')
    StudentLan = self.addSwitch('s2')
    ItLan = self.addSwitch('s3')
    DataCenter = self.addSwitch('s4')
    CoreSwitch = self.addSwitch('s0')
    self.addLink(FacultyLan, CoreSwitch, port1=10, port2=10)
    self.addLink(StudentLan, CoreSwitch, port1=20 , port2=20)
    self.addLink(ItLan, CoreSwitch, port1=30, port2=30)
    self.addLink(DataCenter, CoreSwitch, port1=100, port2=100)
    
     
    # laptop1 = self.addHost('Laptop1', ip='200.20.2.8/24',defaultRoute="Laptop1-eth1")
    
    facutlyWS = self.addHost('facultyWS', ip='10.0.1.2/24', defaultRoute="FacultyWS-eth1", mac='00:00:00:00:00:01')
    self.addLink(facutlyWS, FacultyLan, port1=11, port2=41)
    printer = self.addHost('printer', ip='10.0.1.3/24', defaultRoute="Printer-eth2", mac='00:00:00:00:00:02')
    self.addLink(printer, FacultyLan, port1=12, port2=42)
    facultyPC = self.addHost('facultyPC', ip='10.0.1.4/24', defaultRoute="FacultyPC-eth3", mac='00:00:00:00:00:03')
    self.addLink(facultyPC, FacultyLan, port1=13, port2=43)


    studentPC = self.addHost('studentPC', ip='10.0.2.2/24', defaultRoute="StudentPC-eth4", mac='00:00:00:00:00:04')
    self.addLink(studentPC, StudentLan, port1=21, port2=51)
    labWS = self.addHost('labWS', ip='10.0.2.3/24', defaultRoute="LabWS-eth5", mac='00:00:00:00:00:05')
    self.addLink(labWS, StudentLan, port1=22, port2=52)


    itWS = self.addHost('itWS', ip='10.0.3.2/24', defaultRoute="ItWS-eth6", mac='00:00:00:00:00:06')
    self.addLink(itWS, ItLan, port1=31, port2=61)
    itPC = self.addHost('itPC', ip='10.0.3.3/24', defaultRoute="ItPC-eth7", mac='00:00:00:00:00:07')
    self.addLink(itPC, ItLan, port1=32, port2=62)


    examServer = self.addHost('examServer', ip='10.0.100.2/24', defaultRoute="ExamServer-eth8", mac='00:00:00:00:00:08')
    self.addLink(examServer, DataCenter, port1=81, port2=91)
    webServer = self.addHost('webServer', ip='10.0.100.3/24', defaultRoute="WebServer-eth9", mac='00:00:00:00:00:09')
    self.addLink(webServer, DataCenter, port1=82, port2=92)
    dnsServer = self.addHost('dnsServer', ip='10.0.100.4/24', defaultRoute="DnsServer-eth10", mac='00:00:00:00:00:10')
    self.addLink(dnsServer, DataCenter, port1=83, port2=93)
   
    trustedPC = self.addHost('trustedPC', ip='200.20.203.2/32', defaultRoute="TrustedPC-eth11", mac='00:00:00:00:00:11')
    self.addLink(trustedPC, CoreSwitch, port1=84, port2=94)
    guestPC = self.addHost('guestPC', ip='200.20.198.2/32', defaultRoute="GuestPC-eth12", mac='00:00:00:00:00:12')
    self.addLink(guestPC, CoreSwitch, port1=85, port2=95)
    # switch1 = self.addSwitch('s1')
    
    

 
    
    
    
    
    
    
    
    
    
    
 



    # self.addLink(laptop1, switch1, port1=1, port2=2)

if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
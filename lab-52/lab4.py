#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopology(Topo):
  def __init__(self):
    Topo.__init__(self)
   
    #Switches and links
    coreSwitch =  self.addSwitch('s0')
    facultySwitch = self.addSwitch('s1')
    studentSwitch = self.addSwitch('s2')
    itSwitch = self.addSwitch('s3')
    dataCenterSwitch = self.addSwitch('s4')
    self.addLink(facultySwitch,coreSwitch)
    self.addLink(studentSwitch,coreSwitch)
    self.addLink(itSwitch,coreSwitch)
    self.addLink(dataCenterSwitch,coreSwitch)

    #Internet with links
    trustedPC = self.addHost('trustedPC', ip='10.0.203.2')
    guestPC = self.addHost('guestPC', ip='10.0.198.2')
    self.addLink(trustedPC,coreSwitch)
    self.addLink(guestPC,coreSwitch)

    #Faculty LAN with links
    facultyWS = self.addHost('facultyWS', ip='10.0.1.2/16')
    printer = self.addHost('printer', ip='10.0.1.3/16')
    facultyPC = self.addHost('facultyPC', ip='10.0.1.4/16')
    self.addLink(facultyWS,facultySwitch)
    self.addLink(printer,facultySwitch)
    self.addLink(facultyPC,facultySwitch)

    #Student LAN with links
    studentPC = self.addHost('studentPC', ip='10.0.2.2/16')
    labWS = self.addHost('labWS', ip='10.0.2.3/16')
    self.addLink(studentPC,studentSwitch)
    self.addLink(labWS,studentSwitch)
   
    #IT LAN with links
    itWS = self.addHost('itWS', ip='10.0.3.2/16')
    itPC = self.addHost('itPC', ip='10.0.3.3/16')
    self.addLink(itWS,itSwitch)
    self.addLink(itPC,itSwitch)
   
    #University Data Center with links
    examServer = self.addHost('examServer', ip='10.0.100.2/16')
    webServer = self.addHost('webServer', ip='10.0.100.3/16')
    dnsServer = self.addHost('dnsServer', ip='10.0.100.4/16')
    self.addLink(examServer,dataCenterSwitch)
    self.addLink(webServer,dataCenterSwitch)
    self.addLink(dnsServer,dataCenterSwitch)

   
if __name__ == '__main__':
  #This part of the script is run when the script is executed
  topo = MyTopology() #Creates a topology
  c0 = RemoteController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633) #Creates a remote controller
  net = Mininet(topo=topo, controller=c0) #Loads the topology
  net.start() #Starts mininet
  CLI(net) #Opens a command line to run commands on the simulated topology
  net.stop() #Stops mininet
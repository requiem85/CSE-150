from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
time = "0ms"
bandwidth = "1 Gbps"
class MyTopology(Topo):
  """
  A basic topology
  """
  def __init__(self):
    Topo.__init__(self)
    # Set Up Topology Here
    #setting up switches
    switch = self.addSwitch('switch1') ## Adds a Switch
    switch2 = self.addSwitch('switch2')
    switch3 = self.addSwitch('switch3')
    switch4 = self.addSwitch('switch4')
    #setting up hosts
    siri = self.addHost('Siri', ip='10.0.0.11')
    desktop = self.addHost('Desktop', ip='10.2.0.1')
    fridge = self.addHost('Fridge', ip='10.2.0.2')
    alexa = self.addHost('Alexa', ip='10.3.0.1')
    smarttv = self.addHost('SmartTv', ip='10.3.0.2')
    server = self.addHost('Server', ip='10.4.0.1')
    #adding links
    self.addLink(siri, switch, delay=time, bw=bandwidth)
    self.addLink(desktop, switch2, delay=time, bw=bandwidth)
    self.addLink(fridge, switch2, delay=time, bw=bandwidth)
    self.addLink(alexa, switch3, delay=time, bw=bandwidth)
    self.addLink(smarttv, switch3, delay=time, bw=bandwidth)
    self.addLink(server, switch4, delay=time, bw=bandwidth)
    self.addLink(switch, switch2, delay=time, bw=bandwidth)
    self.addLink(switch2, switch3, delay=time, bw=bandwidth)
    self.addLink(switch3, switch4, delay=time, bw=bandwidth)
    
    
    


    
    
    

if __name__ == '__main__':
  """
  If this script is run as an executable (by chmod +x), this is
  what it will do
  """
  topo = MyTopology() ## Creates the topology
  net = Mininet(topo=topo, link=TCLink ) ## Loads the topology
  net.start() ## Starts Mininet
  # Commands here will run on the simulated topology
  
  CLI(net)
  net.stop() ## Stops Mininet
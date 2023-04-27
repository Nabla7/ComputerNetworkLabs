from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
       h1 = self.addHost('h1')
       h2 = self.addHost('h2')
       h3 = self.addHost('h3')
       
       s1 = self.addSwitch('s1')
       
       r1 = self.addRouter('r1')
       
       ls1h1 = self.addLink('s1', 'h1')
       ls1h2 = self.addLink('s1', 'h2')
       
       lr1s1 = self.addLink('r1', 's1')
       lr1h3 = self.addLink('r1', 'h3')
       
       lr1s1[r1].addParams(ip=("fc00:0:0:1::1/64"))
       lr1h3[r1].addParams(ip=("fc00:0:0:2::1/64"))
              
       super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

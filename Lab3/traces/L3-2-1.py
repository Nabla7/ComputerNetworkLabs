from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
       h1 = self.addHost('h1')
       h2 = self.addHost('h2')
       
       r1 = self.addRouter('r1')
       
       lr1h1 = self.addLink('r1', 'h1')
       lr1h2 = self.addLink('r1', 'h2')
       
       lr1h1[h1].addParams(ip=("fc00:0:0:1::1/64", "10.0.1.1/24"))
       lr1h2[h2].addParams(ip=("fc00:0:0:2::2/64", "10.0.2.2/24"))
       
       lr1h1[r1].addParams(ip=("fc00:0:0:1::10/64", "10.0.1.10/24"))
       lr1h2[r1].addParams(ip=("fc00:0:0:2::10/64", "10.0.2.10/24"))
              
       super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

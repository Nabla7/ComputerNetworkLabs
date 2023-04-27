from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
       h1 = self.addHost('h1')
       h2 = self.addHost('h2')
       h3 = self.addHost('h3')
       h4 = self.addHost('h4')
       
       s1 = self.addSwitch('s1')
       
       ls1h1 = self.addLink('s1', 'h1')
       ls1h2 = self.addLink('s1', 'h2')
       ls1h3 = self.addLink('s1', 'h3')
       ls1h4 = self.addLink('s1', 'h')
       
       ls1h1[h1].addParams(ip=("fc00::1/48", "10.0.0.1/8"))
       ls1h2[h2].addParams(ip=("fc00::2/64", "10.0.0.2/24"))
       ls1h3[h3].addParams(ip=("fc00:0:0:1::3/48", "10.0.255.3/16"))
       ls1h4[h4].addParams(ip=("fc00:0:0:1::4/64", "10.1.0.4/24"))
       
       super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

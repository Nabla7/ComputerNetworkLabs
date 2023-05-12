from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.router.config import RouterConfig, STATIC, StaticRoute

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
       h1 = self.addHost('h1')
       h2 = self.addHost('h2')
       h3 = self.addHost('h3')
       
       r1 = self.addRouter('r1', config=RouterConfig)
       r2 = self.addRouter('r2', config=RouterConfig)
       
       s1 = self.addSwitch('s1')
       
       lh1r1 = self.addLink('h1', 'r1')
       lh3r2 = self.addLink('h3', 'r2')
       lh2s1 = self.addLink('h2', 's1')
       lr1s1 = self.addLink('r1', 's1')
       lr2s1 = self.addLink('r2', 's1')
                  
       lh1r1[h1].addParams(ip=("fc00:0:0:1::1/64"))
       lh1r1[r1].addParams(ip=("fc00:0:0:1::10/64"))
       
       lh3r2[h3].addParams(ip=("fc00:0:0:3::3/64"))
       lh3r2[r2].addParams(ip=("fc00:0:0:3::10/64"))
       
       lh2s1[h2].addParams(ip=("fc00:0:0:2::2/64"))
       
       lr1s1[r1].addParams(ip=("fc00:0:0:2::10/64"))
       lr2s1[r2].addParams(ip=("fc00:0:0:2::11/64"))
       
       super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

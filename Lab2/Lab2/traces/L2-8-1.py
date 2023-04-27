from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
       h1 = self.addHost('h1')
       h2 = self.addHost('h2')
       
       r1 = self.addRouter('r1')
       
       lr1h1 = self.addLink(r1, h1, bw=1, loss=1)
       lr1h2 = self.addLink(r1, h2, bw=1, loss=1)
       
       lr1h1[h1].addParams(ip=("fc00:0:0:1::1/64"))
       lr1h2[h2].addParams(ip=("fc00:0:0:2::2/64"))
       
       lr1h1[r1].addParams(ip=("fc00:0:0:1::10/64"))
       lr1h2[r1].addParams(ip=("fc00:0:0:2::10/64"))
       
       super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    net["h1"].cmd("ethtool -K h1-eth0 tso off")
    net["h2"].cmd("ethtool -K h2-eth0 tso off")
    IPCLI(net)
finally:
    net.stop()

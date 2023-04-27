from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        s1 = self.addSwitch("s1", stp=False)
        
        ls1h1 = self.addLink(s1, h1)
        # Set the IP addresses of host h1
        ls1h1[h1].addParams(ip=("fc00:0:0:1::1/64", "192.168.1.1/24"))
        
        ls1h2 = self.addLink(s1, h2)
        # Set the IP addresses of host h2
        ls1h2[h2].addParams(ip=("fc00:0:0:1::2/64", "192.168.1.2/24"))
        
        super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
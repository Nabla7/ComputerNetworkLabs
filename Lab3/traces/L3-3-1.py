from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopo(IPTopo):

    def build(self, *args, **kwargs):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add switch
        s1 = self.addSwitch('s1')

        # Add router
        r1 = self.addRouter('r1')

        # Add links
        ls1h1 = self.addLink(s1, h1)
        ls1h2 = self.addLink(s1, h2)
        ls1r1 = self.addLink(s1, r1)
        lr1h3 = self.addLink(r1, h3)

        # Set IP addresses
        ls1h1[h1].addParams(ip=("fc00:0:0:1::2/64", "10.0.1.2/24"))
        ls1h2[h2].addParams(ip=("fc00:0:0:1::3/64", "10.0.1.3/24"))
        ls1r1[r1].addParams(ip=("fc00:0:0:1::1/64", "10.0.1.1/24"))
        lr1h3[h3].addParams(ip=("fc00:0:0:2::2/64", "10.0.2.2/24"))
        lr1h3[r1].addParams(ip=("fc00:0:0:2::1/64", "10.0.2.1/24"))

        super().build(*args, **kwargs)

# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
    
        #Hosts
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        h4 = self.addHost("h4")
        h5 = self.addHost("h5")
        h6 = self.addHost("h6")
        
        #Switches
        s1 = self.addSwitch("s1", stp=False)
        s2 = self.addSwitch("s2", stp=False)
        s3 = self.addSwitch("s3", stp=False)
        
        #Router
        r1 = self.addRouter("r1")
        
        #Switch Linking
        h1_s1 = self.addLink(s1, h1)
        h2_s1 = self.addLink(s1, h2)
        
        h3_s2 = self.addLink(s2, h3)
        h4_s2 = self.addLink(s2, h4)
        h5_s2 = self.addLink(s2, h5)
        
        h6_s3 = self.addLink(s3, h6)
        
        #Router Linking
        r1_s1 = self.addLink(r1, s1)
        r1_s2 = self.addLink(r1, s2)
        r1_s3 = self.addLink(r1, s3)
        
        
        #Setting IP
        h1_s1[h1].addParams(ip="fc00:0:0:1::1/64")
        h2_s1[h2].addParams(ip="fc00:0:0:1::2/64")
        h3_s2[h3].addParams(ip="fc00:0:0:2::1/64")
        h4_s2[h4].addParams(ip="fc00:0:0:2::2/64")
        h5_s2[h5].addParams(ip="fc00:0:0:2::3/64")
        h6_s3[h6].addParams(ip="fc00:0:0:3::1/64")
        
        r1_s1[s1].addParams(ip="fc00:0:0:1::10/64")
        r1_s2[s2].addParams(ip="fc00:0:0:2::10/64")
        r1_s3[s3].addParams(ip="fc00:0:0:3::10/64")
    
        super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

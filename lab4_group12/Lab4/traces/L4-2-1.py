from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.router.config import RouterConfig, STATIC, StaticRoute

class MyTopo( IPTopo ):
    
    def build(self, *args, **kwargs):
       h1 = self.addHost('h1', cwd='./')
       h2 = self.addHost('h2', cwd='./')
       
       r1 = self.addRouter('r1', config=RouterConfig, cwd='./')
       r2 = self.addRouter('r2', config=RouterConfig, cwd='./')
       r3 = self.addRouter('r3', config=RouterConfig, cwd='./')
       r4 = self.addRouter('r4', config=RouterConfig, cwd='./')       
      
       
       lh1r1 = self.addLink('h1', 'r1')
       lh2r3 = self.addLink('h2', 'r3')
       
       lr1r2 = self.addLink('r1', 'r2')
       lr1r4 = self.addLink('r1', 'r4')
       lr2r4 = self.addLink('r2', 'r4')
       lr2r3 = self.addLink('r2', 'r3')
       
       
       lh1r1[h1].addParams(ip=("fc00:0:0:1::1/64"))
       lh1r1[r1].addParams(ip=("fc00:0:0:1::11/64"))       

       lh2r3[h2].addParams(ip=("fc00:0:0:6::2/64"))
       lh2r3[r3].addParams(ip=("fc00:0:0:6::13/64"))
       
       lr1r2[r1].addParams(ip=("fc00:0:0:2::11/64"))
       lr1r2[r2].addParams(ip=("fc00:0:0:2::12/64"))
       
       lr1r4[r1].addParams(ip=("fc00:0:0:5::11/64"))
       lr1r4[r4].addParams(ip=("fc00:0:0:5::14/64"))
       
       lr2r4[r2].addParams(ip=("fc00:0:0:4::12/64"))
       lr2r4[r4].addParams(ip=("fc00:0:0:4::14/64"))
       
       lr2r3[r2].addParams(ip=("fc00:0:0:3::12/64"))
       lr2r3[r3].addParams(ip=("fc00:0:0:3::13/64"))       
              
       # self.addNetworkCapture(nodes=[], base_filename="capture")
       
       super().build(*args, **kwargs)
        
# Create a network using the topology you just created and run IPMininet        
net = IPNet(topo=MyTopo(), allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()

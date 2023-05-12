import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config import RouterConfig, BGP, iBGPFullMesh, AS, bgp_peering, OSPF6
import ipmininet.router.config.bgp as _bgp
from ipmininet.iptopo import IPTopo

class BGPOSPF(IPTopo):

    def build(self, *args, **kwargs):
        # BGP routers
        # AS 1
        as1ra = self.bgp('as1ra', ['fc00:0:1:a::/64'])
        as1rb = self.bgp('as1rb', ['fc00:0:1:b::/64'])
        as1rc = self.bgp('as1rc', ['fc00:0:1:c::/64'])
        as1rd = self.bgp('as1rd', ['fc00:0:1:d::/64'])
        # AS 2
        as2ra = self.bgp('as2ra', ['fc00:0:2:a::/64'])
        as2rb = self.bgp('as2rb', ['fc00:0:2:b::/64'])
        as2rc = self.bgp('as2rc', ['fc00:0:2:c::/64'])
        as2rd = self.bgp('as2rd', ['fc00:0:2:d::/64'])
        # AS 3
        as3ra = self.bgp('as3ra', ['fc00:0:3:a::/64'])
        as3rb = self.bgp('as3rb', ['fc00:0:3:b::/64'])
        as3rc = self.bgp('as3rc', ['fc00:0:3:c::/64'])
        as3rd = self.bgp('as3rd', ['fc00:0:3:d::/64'])

        # Intra-AS links
        self.addLink(as1ra, as1rb,
                    params1={"ip":"fc00:0:1:ab::a/64"},
                    params2={"ip":"fc00:0:1:ab::b/64"})
        
        self.addLink(as1ra, as1rd,
                    params1={"ip":"fc00:0:1:ad::a/64"},
                    params2={"ip":"fc00:0:1:ad::d/64"})
        self.addLink(as1rb, as1rc,
                    params1={"ip":"fc00:0:1:bc::b/64"},
                    params2={"ip":"fc00:0:1:bc::c/64"})
        
        self.addLink(as1rc, as1rd,
                    params1={"ip":"fc00:0:1:cd::c/64"},
                    params2={"ip":"fc00:0:1:cd::d/64"})
        
        self.addLink(as2ra, as2rb,
                    params1={"ip":"fc00:0:2:ab::a/64"},
                    params2={"ip":"fc00:0:2:ab::b/64"})
        
        self.addLink(as2ra, as2rd,
                    params1={"ip":"fc00:0:2:ad::a/64"},
                    params2={"ip":"fc00:0:2:ad::d/64"})
        self.addLink(as2rb, as2rc,
                    params1={"ip":"fc00:0:2:bc::b/64"},
                    params2={"ip":"fc00:0:2:bc::c/64"})
        
        self.addLink(as2rc, as2rd,
                    params1={"ip":"fc00:0:2:cd::c/64"},
                    params2={"ip":"fc00:0:2:cd::d/64"})

        self.addLink(as3ra, as3rb,
                    params1={"ip":"fc00:0:3:ab::a/64"},
                    params2={"ip":"fc00:0:3:ab::b/64"})
        
        self.addLink(as3ra, as3rd,
                    params1={"ip":"fc00:0:3:ad::a/64"},
                    params2={"ip":"fc00:0:3:ad::d/64"})
        self.addLink(as3rb, as3rc,
                    params1={"ip":"fc00:0:3:bc::b/64"},
                    params2={"ip":"fc00:0:3:bc::c/64"})
        
        self.addLink(as3rc, as3rd,
                    params1={"ip":"fc00:0:3:cd::c/64"},
                    params2={"ip":"fc00:0:3:cd::d/64"})

        # Inter-AS links
        las1as2 = self.addLink(as1rc, as2ra,
                               params1={"ip": "fc00:12::c/64"},
                               params2={"ip": "fc00:12::a/64"},
                               igp_passive=True)
                               
        las2as3 = self.addLink(as2rc, as3ra,
                               params1={"ip": "fc00:23::c/64"},
                               params2={"ip": "fc00:23::a/64"},
                               igp_passive=True)
        las1as3 = self.addLink(as3rc, as1ra,
                               params1={"ip": "fc00:13::c/64"},
                               params2={"ip": "fc00:13::a/64"},
                               igp_passive=True)
                               

        # Set AS-ownerships
        self.addiBGPFullMesh(1, routers=[as1ra, as1rb, as1rc, as1rd])
        self.addiBGPFullMesh(2, routers=[as2ra, as2rb, as2rc, as2rd])
        self.addiBGPFullMesh(3, routers=[as3ra, as3rb, as3rc, as3rd])

        # Add eBGP peering
        bgp_peering(self, as1rc, as2ra)
        bgp_peering(self, as2rc, as3ra)
        bgp_peering(self, as3rc, as1ra)

        # OSPF configuration
        as1ra.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as1rb.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as1rc.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as1rd.addDaemon(OSPF6, hello_int=5, dead_int=20)

        as2ra.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as2rb.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as2rc.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as2rd.addDaemon(OSPF6, hello_int=5, dead_int=20)

        as3ra.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as3rb.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as3rc.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as3rd.addDaemon(OSPF6, hello_int=5, dead_int=20)

        # Hosts attached to the routers
        self.addLink(as1ra, self.addHost('h1a'),
                     params1={"ip": "fc00:0:1:a::a/64"},
                     params2={"ip": "fc00:0:1:a::1/64"})
        self.addLink(as1rb, self.addHost('h1b'),
                     params1={"ip": "fc00:0:1:b::b/64"},
                     params2={"ip": "fc00:0:1:b::1/64"})
        self.addLink(as1rc, self.addHost('h1c'),
                     params1={"ip": "fc00:0:1:c::c/64"},
                     params2={"ip": "fc00:0:1:c::1/64"})
        self.addLink(as1rd, self.addHost('h1d'),
                     params1={"ip": "fc00:0:1:d::d/64"},
                     params2={"ip": "fc00:0:1:d::1/64"})

        self.addLink(as2ra, self.addHost('h2a'),
                     params1={"ip": "fc00:0:2:a::a/64"},
                     params2={"ip": "fc00:0:2:a::2/64"})
        self.addLink(as2rb, self.addHost('h2b'),
                     params1={"ip": "fc00:0:2:b::b/64"},
                     params2={"ip": "fc00:0:2:b::2/64"})
        self.addLink(as2rc, self.addHost('h2c'),
                     params1={"ip": "fc00:0:2:c::c/64"},
                     params2={"ip": "fc00:0:2:c::2/64"})
        self.addLink(as2rd, self.addHost('h2d'),
                     params1={"ip": "fc00:0:2:d::d/64"},
                     params2={"ip": "fc00:0:2:d::2/64"})

        self.addLink(as3ra, self.addHost('h3a'),
                     params1={"ip": "fc00:0:3:a::a/64"},
                     params2={"ip": "fc00:0:3:a::3/64"})
        self.addLink(as3rb, self.addHost('h3b'),
                     params1={"ip": "fc00:0:3:b::b/64"},
                     params2={"ip": "fc00:0:3:b::3/64"})
        self.addLink(as3rc, self.addHost('h3c'),
                     params1={"ip": "fc00:0:3:c::c/64"},
                     params2={"ip": "fc00:0:3:c::3/64"})
        self.addLink(as3rd, self.addHost('h3d'),
                     params1={"ip": "fc00:0:3:d::d/64"},
                     params2={"ip": "fc00:0:3:d::3/64"})

        super(BGPOSPF, self).build(*args, **kwargs)

    def bgp(self, name, net=None):
        if net is None:
            net = []
        return self.addRouter(name, use_v4=True,
                              use_v6=True,
                              config=(RouterConfig,
                                      {'daemons': [(BGP,
                                                    {'address_families': (_bgp.AF_INET6(networks=net),)}
                                                    ), 
                                                    OSPF6
                                                    ]
                                       }
                                      )
                              )

# Start network
net = IPNet(topo=BGPOSPF(), use_v4=False, use_v6=True, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()

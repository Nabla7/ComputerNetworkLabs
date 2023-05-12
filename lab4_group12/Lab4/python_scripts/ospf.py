import argparse
import json
import os
from mininet.log import LEVELS, lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config.zebra import Zebra
from ipmininet.iptopo import IPTopo
from ipmininet.utils import realIntfList

from ipmininet.router.config import RouterConfig, OSPF6

"""This file contains a simple network using OSPF"""

class SimpleOSPF(IPTopo):

    def build(self, *args, **kwargs):
        # OSPF routers
        as1ra = self.addRouter("as1ra", config=RouterConfig)
        as1rb = self.addRouter("as1rb", config=RouterConfig)
        as1rc = self.addRouter("as1rc", config=RouterConfig)
        as1rd = self.addRouter("as1rd", config=RouterConfig )

        lrarb = self.addLink(as1ra, as1rb, igp_metric=1,
                    params1={"ip":"fc00:0:1:ab::a/64"},
                    params2={"ip":"fc00:0:1:ab::b/64"})
        self.addLink(as1ra, as1rc, igp_metric=2,
                    params1={"ip":"fc00:0:1:ac::a/64"},
                    params2={"ip":"fc00:0:1:ac::c/64"})
        self.addLink(as1ra, as1rd, igp_metric=3,
                    params1={"ip":"fc00:0:1:ad::a/64"},
                    params2={"ip":"fc00:0:1:ad::d/64"})
        self.addLink(as1rb, as1rc, igp_metric=4,
                    params1={"ip":"fc00:0:1:bc::b/64"},
                    params2={"ip":"fc00:0:1:bc::c/64"})
        self.addLink(as1rb, as1rd,  igp_metric=5,
                    params1={"ip":"fc00:0:1:bd::b/64"},
                    params2={"ip":"fc00:0:1:bd::d/64"})
        self.addLink(as1rc, as1rd,  igp_metric=6,
                    params1={"ip":"fc00:0:1:cd::c/64"},
                    params2={"ip":"fc00:0:1:cd::d/64"})

        as1ra.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as1rb.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as1rc.addDaemon(OSPF6, hello_int=5, dead_int=20)
        as1rd.addDaemon(OSPF6, hello_int=5, dead_int=20)
        

        # hosts attached to the routers
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

        self.addNetworkCapture(interfaces=[lrarb[as1ra]],
                                base_filename="ospf",
                                extra_arguments="-v")
        
        super(SimpleOSPF, self).build(*args, **kwargs)

# Start network
net = IPNet(topo=SimpleOSPF(), use_v4=False, use_v6=True, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()

#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import LinearTopo

#Especifica el tipo de topologia
#Linear = LinearTopo(k=4)
#net = Mininet(topo=Linear)

topos = { 'mytopo': (lambda: LinearTopo(k=4) ) }


#net.start()
#net.pingAll()
#net.stop()


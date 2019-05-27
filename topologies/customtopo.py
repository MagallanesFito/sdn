from mininet.net import Mininet
from mininet.topo import Topo

class CustomTopo(Topo):
	def __init__(self):
		#Crear nodos en la red
		c0 = net.addController()
		h0 = net.addHost('h0')
		s0 = net.addSwitch('s0')
		h1 = net.addHost('h1')

		#Agregar enlaces
		net.addLink(h0,s0)
		net.addLink(h1,s0)

		#Configurar direcciones ip
		h0.setIP('192.168.1.1',24)
		h1.setIP('192.168.1.2',24)
topos = {'mytopo':(lambda: CustomTopo())}


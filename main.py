#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import json
import unicodedata
from subprocess import Popen, PIPE
import time
#import networkx as nx
from sys import exit

''' un grafo de aristas de la forma (origen,destino)'''
switch = {}
deviceMAC = {}
deviceIP = {}
hostPorts = {}
''' Metodo para obtener la informacion 
codificada como json'''
def getResponse(url):
        response = requests.get(url,auth=HTTPBasicAuth('admin','admin'))
        ''' Obtiene la informacion sobre la peticion que se realiza'''
        if(response.ok):
                encoded_response = json.loads(response.content)
                return encoded_response
                #createGraph(encoded_response)
        else:
                print("No se ha obtenido informacion")
                response.raise_for_status()
                return None
'''def calculateCost(data):
        cost = 0

        for i in data["node-connector"]:
                transmitted = i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["transmitted"]
                transmitted = int(transmitted)
                received = i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["received"]
                received = int(received)
                rate  = transmitted+receivd

        for i in data["node-connector"]:
                transmitted = i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["transmitted"]
                transmitted = int(transmitted)
                received = i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["received"]
                received = int(received)
                cost = transmitted+received 
        return cost'''
def createGraph(data):
        G = []
        #Obtener informacion de MAC e ip
        for i in data["network-topology"]["topology"]:
                for j in i["node"]:
                        if "host-tracker-service:addresses" in j:
                                for k in j["host-tracker-service:addresses"]:
                                        ip = k["ip"].encode('ascii','ignore')
                                        mac = k["mac"].encode('ascii','ignore')
                                        deviceMAC[ip]  = mac
                                        deviceIP[mac] = ip
                        if "host-tracker-service:attachment-points" in j:
                                for k in j["host-tracker-service:attachment-points"]:
                                        mac = k["corresponding-tp"].encode('ascii','ignore')
                                        mac = mac.split(":",1)[1]
                                        ip = deviceIP[mac]
                                        temp = k["tp-id"].encode('ascii','ignore')
                                        switchID = temp.split(":")
                                        port = switchID[2]
                                        hostPorts[ip] = port
                                        switchID = switchID[0]+":"+switchID[1]
                                        switch[ip] = switchID
        #Construye el grafo de la red
        print("Construyendo grafo de red.....")
        for stat in data["network-topology"]["topology"]:
                for link in stat["link"]:
                        if "host" not in link["link-id"]:
                                src = link["link-id"].encode('ascii','ignore').split(":")
                                #srcPort = src[2]
                                dst = link["destination"]["dest-tp"].encode('ascii','ignore').split(":")
                                #dstPort = dst[2]
                                srcToDst = src[1] + "::" + dst[1]
                                #linkPorts[srcToDst] = srcPort + "::" + dstPort
                                src_dest_tuple = ((int)(src[1]),(int)(dst[1]))
                                G.append(src_dest_tuple)

        #Regresa el grafo
        return G
        #imprime el grafo
        #print("Grafo.................")
        #print(G)
        #print("Origen--------")
        #s = "10.0.0.1"
        #d = "10.0.0.3"
        #origen = int(switch[s].split(":",1)[1])
        #print(origen)
        #print("Destino--------")
        #destino = int(switch[d].split(":",1)[1])
        #print(destino)
        '''Mapeo de ip : mac
        print("Device IP y mac.......")
        print(deviceMAC)
        switch a dispositivo
        print("switch: device mapping")
        print(switch)'''
#Main

print("Inicia el programa principal")
port = "8181"
host = "http://192.168.56.101"
operations =[ "/restconf/operational/network-topology:network-topology","/restconf/config/1"]
url =  host+":"+port+operations[0]
#print(url)
res = getResponse(url)
if res != None:
        grafo = createGraph(res)
print(grafo)
#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import json
from GraphAlgorithm import GraphAlgorithm

''' un grafo de aristas de la forma (origen,destino)'''
linkPorts = {}
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
def calculateCost(data,rate):
        cost = 0
        if rate=='tx':
                transmitted = int(data["node-connector"][0]["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["transm$
                cost  = transmitted
        elif rate=='rx':
                received  = int(data["node-connector"][0]["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["received$
                cost  = received
        return cost
def createGraph(data):
        G = []
        #Construye el grafo de la red
        for stat in data["network-topology"]["topology"]:
                for link in stat["link"]:
                        if "host" not in link["link-id"]:
                                src = link["link-id"].encode('ascii','ignore').split(":")
                                srcPort = src[2]
                                dst = link["destination"]["dest-tp"].encode('ascii','ignore').split(":")
                                dstPort = dst[2]
                                srcToDst = src[1] + "::" + dst[1]
                                linkPorts[srcToDst] = srcPort+"::"+dstPort
                                src_dest_tuple = ((int)(src[1]),(int)(dst[1]))
                                G.append(src_dest_tuple)

        #Regresa el grafo
        return G
#Main---------------------------------------------------

port = "8181"
host = "http://192.168.56.101"
operations =[ "/restconf/operational/network-topology:network-topology","/restconf/config/1"]
url =  host+":"+port+operations[0]

res = getResponse(url)
if res != None:
        grafo = createGraph(res)
print("Grafo construido")
print(grafo)
#-------------------------------------------------
'''Ejemplo, crear una instancia de GraphAlgorithm para obtener todas las rutas desde h1 a h2 
y para cada una de las rutas obtener el tx rate
'''
algo = GraphAlgorithm(grafo)
#Origen
h1 = 1
#Destino
h2 = 3
#Obtener todas las rutas
all_paths = algo.all_paths(h1,h2)

#Itera por todas las rutas
i = 0

type_rate = 'tx'
for path in all_paths:
        print("ruta: "+str(i))
        for node in range(len(path)):
                if node == len(path)-1:
                        curr_key = str(path[node])+"::"+str(path[node-1])
                else:
                        curr_key = str(path[node])+"::"+str(path[node+1])
                curr_port = linkPorts[curr_key]
                curr_port = str(curr_port.split(":",1)[0])
                current_node = str(path[node])
                curr_url = "http://192.168.56.101:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:"\
                +current_node+"/node-connector/openflow:"+current_node+":"+curr_port
                res = getResponse(curr_url)
                #Calcula el tx del i-esimo nodo
                mycost = calculateCost(res,type_rate)
                print("\t nodo: "+current_node+"------ "+type_rate+" rate: "+str(mycost))
        i = i+1


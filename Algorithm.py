#biblioteca de grafos
#Grafo de prueba
#G = [(1,2),(2,1),(1,3),(3,1),(3,4),(4,3),(2,4),(4,2),(1,4),(4,1)]
#G  = [(1, 2), (2, 1), (3, 2), (2, 3)]

class GraphAlgoritm:
        def __init__(self,g):
            self.adjency_list = self.buildAdjencyList(g)
            self.all_paths_list = [] 
        ''' getter de array de todas las rutas'''
        def get_all_paths(self):
            return self.all_paths_list
        def getNumNodes(self,g):
                max_ = 0
                for e in g:
                        maxLocal = max(e)
                        if maxLocal > max_:
                                max_ = maxLocal
                return max_
        def buildAdjencyList(self,g):
                adjList = {}
                for edge in g:
                        a = edge[0]
                        b = edge[1]
                        if a not in adjList.keys():
                                adjList[a] = []
                        adjList[a].append(b)
                return adjList       
        ''' Realiza una bfs desde el nodo origen src
        hasta destino dest'''
        def shortest_path(self,src,dest):
            queue = []
            queue.append([src])
            visited = set()
            #adjency_list = self.buildAdjencyList(g)
            while queue:
                path= queue.pop(0)
                node = path[-1]
                if node == dest:
                    return path
                elif node not in visited:
                    for adjacent in self.adjency_list.get(node,[]):
                        new_path = list(path)
                        new_path.append(adjacent)
                        queue.append(new_path)
                    visited.add(node)
        ''' Realiza una dfs desde el origen src
        hasta destino dest'''
        def all_paths_util(self,src,dest,visited,path):
            visited.add(src)
            path.append(src)
            
            if src == dest:
                #print(path)
                self.all_paths_list.append(path[:])
            else:
                for adjacent in self.adjency_list.get(src,[]):
                    if adjacent not in visited:
                        self.all_paths_util(adjacent,dest,visited,path)
            path.pop()
            visited.remove(src)
        def all_paths(self,src,dest):
            visited = set()
            path = []
            #adjency_list = self.buildAdjencyList(g)
            self.all_paths_util(src,dest,visited,path)
            return self.all_paths_list

#algo  = GraphAlgoritm(G)
#src = 1
#dest = 4

#print(algo.all_paths(src,dest))
#print("La ruta mas corta desde %d hacia %d es %d "%(src,dest,best_dist))
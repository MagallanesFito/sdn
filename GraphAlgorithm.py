#biblioteca de grafos

INF = (2<<32)
class GraphAlgorithm:
	'''El constructor recibe como parametro un grafo representado 
	como una lista de aristas, de la siguiente forma: 
	[(origen1,destino1),(origen2,destino2),(origen3,destino3)...]'''
        def __init__(self,g):
            #Representacion en lista de adyacencia
            self.adjency_list = self.build_adjency_list(g)
            self.all_paths_list = [] 
            #numero de nodos del grafo
            self.V = self.get_num_nodes(g)
            #Representacion en matriz de adyacencia
            self.adjency_matrix = self.adjency_list_to_matrix()
            #self.INF = 1000000
        ''' getter de array de todas las rutas'''
        def get_all_paths(self):
            return self.all_paths_list
        ''' Funcion auxiliar para convertir una lista de  
        adyacencia en una matriz de adyacencia'''
        def adjency_list_to_matrix(self):
            matrix = [[INF for i in range(self.V)] for j in range(self.V)]
            for key,value in self.adjency_list.items():
                for node in value:
                    matrix[key-1][node-1] = 1
            for i in range(self.V):
                matrix[i][i] = 0
            return matrix
        '''Funcion auxiliar para imprimir una matriz de adyacencia'''
        def print_adjcency_matrix(self):
            for i in range(self.V):
                for j in range(self.V):
                    print(str(self.adjency_matrix[i][j])+" ",end='')
                print("\n")
        '''Dado un grafo representado como una lista de vertices
        obtener el numero de nodos en el grafo.
        '''
        def get_num_nodes(self,g):
                max_ = 0
                for e in g:
                        maxLocal = max(e)
                        if maxLocal > max_:
                                max_ = maxLocal
                return max_
        ''' Dado un grafo representado como un conjunto de 
        aristas, convertirlo en una lista de adyacencia'''
        def build_adjency_list(self,g):
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
        ''' Obtener todas las rutas de un vertice a otro'''
        def all_paths_util(self,src,dest,visited,path):
            visited.add(src)
            path.append(src)
            
            if src == dest:
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
            
            self.all_paths_util(src,dest,visited,path)
            return self.all_paths_list
        ''' Funcion auxiliar para imprimir una matriz de distancias
        mas cortas.'''
        def print_solution(self,matrix):
            for i in range(self.V):
                for j in range(self.V):
                    if self.distances[i][j] == INF:
                        print("INF ",end='')
                    else: 
                        print(str(self.distances[i][j])+" ",end='')
                print("\n")
        ''' Realiza el algoritmo de floyd warshall para 
        obtener una matriz de rutas mas cortas entre todos
        los pares de nodos en O(V^3)'''
        def all_pairs_shortest_path(self):
            distances = []
            #Inicializa la matriz de distances
            for i in range(self.V):
                distances.append([])
                for j in range(self.V):
                    distances[i].append(self.adjency_matrix[i][j])
            #Realiza la programacion dinamica
            for k in range(self.V):
                for i in range(self.V):
                    for j in range(self.V):
                        distances[i][j] = min(distances[i][j],distances[i][k]+distances[k][j])
            #Imprime solucion
            #self.print_solution(self.distances)
            return distances

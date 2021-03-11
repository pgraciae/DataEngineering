import numpy as np
import os
import time
path = 'Tests_v1/Grafo4.txt'
import copy
import operator
import functools
import copy
class Graph:

    class element:
        def __init__(self,element,val,track):
            self.track = track
            self.elem = element
            self.val = val

    class queue:
        def __init__(self):
            self._queue = []
        def append(self,element):
            if self._queue == []:
                self._queue = [element]
            else:

                for x,y in enumerate(self._queue):
                    if element.val > y.val:
                        index = x
                        break
                self._queue.insert(x,element)
        def __len__(self):
            return len(self._queue)
        def is_empty(self):
            return True if self._queue==[] else False

        def pop(self):
            return self._queue.pop()

        def __repr__(self):
            print(f'{[x.elem.pos for x in self._queue]}')
        def __str__(self):
            return str([x.elem for x in self._queue])

    class Edge:
        __slots__ = ['coor_or', 'coor_dest', 'distance']

        def __init__(self, cor_or, cor_dest, distance):
            self.coor_or = cor_or
            self.coor_dest = cor_dest
            self.distance = distance

    class Node:
        __slots__ = ['pos']

        def __init__(self, pos):
            self.pos = pos

        def __hash__(self):
            return hash(self.pos)

        def __eq__(self, other):
            if type(other) == type(self):
                return self.pos == other.pos
            if type(other) == type((1, 2)):
                return self.pos == other

    __slots__ = ['nodes', 'positions', 'counter_nodes']

    def __init__(self, file=None, dic={}):
        self.positions = {}
        self.counter_nodes = 0

        if dic:
            self.nodes = dic
        if file != None:
            if not dic:self.nodes={}
            self.read_txt(file)


    def set_node(self, attrs):
        node_to_append = self.Node((attrs[0], attrs[1]))
        if node_to_append not in self.nodes: self.nodes.__setitem__(node_to_append, {})
        return True

    def set_nodes(self, list_nodes):
        ##Formato nodo = ['name',posx,posy]
        for x, y in list_nodes:
            self.set_node(x, y)
        return True

    def eu_dist(self,array):
        return sum([np.sqrt((array[x][0] - array[x + 1][0]) ** 2 + (array[x][1] - array[x + 1][1]) ** 2) for x in
                    range(len(array) - 1)])

    def set_edges(self, list_edges):
        for x, y in list_edges:
            self.set_edge(x, y)

    def set_edge(self, edge):
        x, y = edge
        dist = self.euclidian(x, y)
        if x not in self.nodes: self.set_node(x)
        if y not in self.nodes: self.set_node(y)
        self.nodes[self.Node(x)][self.Node(y)] = self.Edge(x, y, dist)
        self.nodes[self.Node(y)][self.Node(x)] = self.Edge(y, x, dist)

    def euclidian(self, a, b):

        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)

    def get_matrix(self):
        matrix_temp = np.zeros((self.counter_nodes, self.counter_nodes))
        for x in self.nodes:
            for y in self.nodes[x]:
                matrix_temp[self.positions[x.pos]][self.positions[y.pos]] = self.nodes[x][y].distance
        return matrix_temp

    def sort_by_indexes(self,array,indexes):
        elements = array[indexes]
        elements,indexes = zip(*sorted(zip(elements,indexes)))
        for x,y in zip(indexes,elements):
            yield y,x

    def dijkstra(self, inicial):
        visitats = []
        matriu_dist = self.get_matrix()
        vect_res = np.zeros(self.counter_nodes)
        vect_res[:] = np.inf
        index_inicial = self.positions[inicial]
        vect_res[index_inicial] = 0
        while len(visitats) != self.counter_nodes:
            distancia_actual = vect_res[index_inicial]
            minim_no_visitat = np.inf
            index_a_nodes = [x for x in self.nodes if index_inicial == self.positions[x]][0]
            for adjacent in self.nodes[index_a_nodes]:

                if adjacent not in visitats:
                    index_adjacent = self.positions[adjacent]
                    dtemp = distancia_actual + matriu_dist[index_inicial][index_adjacent]

                    if dtemp < vect_res[index_adjacent]:
                        vect_res[index_adjacent] = dtemp

                    if minim_no_visitat > dtemp:
                        index_a_visitar = index_adjacent
                        minim_no_visitat = dtemp

            if (index_inicial not in visitats):
                visitats.append(index_inicial)
            else:
                index_a_visitar = [self.positions[x] for x in self.positions if
                                   self.positions[x] not in visitats and vect_res[self.positions[x]] != np.inf][0]
            index_inicial = index_a_visitar
        return vect_res

    def get_nearest_pref(self,city,preferences,desti):
        dijkstra = self.dijkstra(city)
        min=100000
        pos_min=0
        nodes = [y for y in self.nodes]
        for t in [x for x,y in enumerate(preferences)]:

            if dijkstra[preferences[t][1]]<min and nodes[preferences[t][1]]!=desti and dijkstra[preferences[t][1]]>0:
                min = dijkstra[preferences[t][1]]
                node = nodes[preferences[t][1]]

        return node

    def Greedy(self, inici, desti, visits):
        nodes = [x for x in self.nodes]
        preferences = [(y,x) for x,y in enumerate(self.nodes) if y in visits  ][:]
        preferences2 = [y for x, y in enumerate(self.nodes) if y in visits ][:]
        track = [inici]
        if len(visits)==2 and desti in self.nodes[inici]:
            return [inici,desti]

        while preferences2:
            city_to_go=0
            flag=False
            city_to_go = self.get_nearest_pref(inici,preferences,desti if len(preferences)>1 else None)
            for vei_inici in self.nodes[inici]:

                if vei_inici == city_to_go:
                    track.append(city_to_go.pos)
                    inici = city_to_go.pos
                    preferences = [ x for x in preferences if x[0] != city_to_go]
                    preferences2.remove(city_to_go)
                    flag=True

            if not flag:

                cost_inici = self.dijkstra(inici)
                veins = [x for x in self.nodes[inici]]
                veins_idx = [idx for x in veins for idx,y in enumerate(nodes) if y==x]
                dijk = self.dijkstra(city_to_go)
                inici_pos = [x for x, y in enumerate(nodes) if y == city_to_go][0]
                dijk[inici_pos] = np.inf
                min=100000
                index= None
                for x in veins_idx:
                    if (dijk[x]+cost_inici[x])<min:
                        min=dijk[x]+cost_inici[x]
                        index=x
                nodeAct = nodes[index]

                track.append(nodeAct.pos)
                inici = nodeAct
        return track

    def BackTracking(self,inici,visits,track,desti,nodes):
            if len(visits) == 1:
                return track,visits
            else:
                if type(inici)==type(self.Node([1,1])):
                    inici = inici.pos
                city_to_go = min(visits,key = lambda x: (x[0]-inici[0])**2+ (x[1]-inici[1])**2 if x != track[0] else 1000000000)
                dijkstra_to_go = self.dijkstra(city_to_go)
                dijkstra = self.dijkstra(inici)
                index_to_go = [t[0] for t in nodes if city_to_go==t[1]][0]

                for x in self.nodes[inici]:

                    if x==city_to_go:
                        visits.remove(city_to_go)
                        track.append(city_to_go)
                        track, visits = self.BackTracking(x, visits, track, desti,nodes)
                        if track[-1]==desti  and len(visits)==1:
                            return track,visits
                        visits.append(city_to_go)
                        track.remove(city_to_go)

                    else:
                        index_x = [t[0] for t in nodes if x==t[1]][0]
                        #Condicio backtracking optim
                        if int(dijkstra_to_go[index_x]+dijkstra[index_x]) == int(dijkstra[index_to_go]):
                            track.append(x.pos)
                            track, visits = self.BackTracking(x, visits, track, desti,nodes)
                            if track[-1] == desti and len(visits) == 1:
                                return track, visits
                            track.remove(x.pos)
                        else:
                            continue
            return track, visits
            

    def BackTrackingGreedy(self,inici,desti,visits):
        track = [inici]
        #visits.remove(inici)
        nodes = [(x,y) for x,y in enumerate(self.nodes)]
        return self.BackTracking(inici,visits,track,desti,nodes)


    def BackTracking0(self, inici, visits, track, desti, nodes, dist, visits2, track_def, inici0):  #mirar si el track te la llarfada del trackoptim

        if self.eu_dist(track) < dist and len(visits) == 0 and track[-1] == desti: # and len(track) ==3:
            dist = self.eu_dist(track)
            track_def = copy.deepcopy(track)
            return track_def, dist
        
        else:
 
            for x in self.nodes[inici]:
                
                    track.append(x.pos)
                   
                    visits = [v for v in visits if v != x.pos]

                    if self.eu_dist(track) < dist and track[0] == inici0 and len(track) < 20:
     
                        track_def, dist = self.BackTracking0(x, visits, track, desti, nodes, dist, visits2, track_def, inici0)
    
                        track.reverse()
                        track.remove(x.pos)
                        track.reverse()

                        if x.pos in visits2:
                            visits.append(x.pos) 
                            
                    else:
                        
                        track.reverse()
                        track.remove(x.pos)
                        track.reverse()
                        
                        if x.pos in visits2:
                            visits.append(x.pos)          

        return track_def, dist

        

    def BackTrackingPur(self, inici, desti, visits):
        dist = 142000
        inici0 = copy.deepcopy(inici)
        track = [inici]
        track_nodes = [inici]
        nodes = [(x, y) for x, y in enumerate(self.nodes)]
        visits2 = copy.deepcopy(visits)
        track_def = [inici]
        return self.BackTracking0(inici, visits, track, desti, nodes, dist, visits2, track_def, inici0)


    def dist(self,a,b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2

    def ramifica(self,node,queue,visits):
        for y in self.nodes[node.elem]:
                dist = self.dist(node.elem.pos if type(node.elem)!=tuple else node.elem, y.pos)

                d2 = [x.pos for x in self.nodes[y]]

                d3 = functools.reduce(operator.add,[list(self.nodes[x].keys()) for x in d2])
                #d3 = [x.pos for x in d3]

                if (y in visits or any([t in self.nodes[y] for t in visits]))  :
                    el = self.element(y,node.val+dist/len([x for x in visits if x in node.track ]),node.track+[y] if y!=node.track[-1] else node.track)

                    queue.append(el)
                #else:queue.append(self.element(y, node.val + dist, node.track + [y]))
        return queue
    def get_path(self,a,b):
        path = [a.pos if type(a)!=tuple else a,]
        distances = self.dijkstra(a)
        indexes = [x for x,y in enumerate(self.nodes) if y==b][0]
        indexes1 = [x for x, y in enumerate(self.nodes) if y == a][0]
        dist_to_destiny = distances[indexes]
        nodeAct=a
        while path[-1]!=b:
            if b in self.nodes[nodeAct]:
                return path+[b]
            for x in self.nodes[nodeAct]:
                indexe = [t  for t, y in enumerate(self.nodes) if y == x][0]
                dist2 = self.dijkstra(x)[indexes]
                if np.allclose(dist_to_destiny, distances[indexe] + dist2):
                    path.append(x.pos)
                    break
            nodeAct=path[-1]






    def B_B1(self,inici,desti,visits1):
        nodes = [(x,y) for x,y in enumerate(self.nodes)]
        queue = self.queue()
        inici = [x for x in nodes if x[1]==inici][0][1]
        queue.append(self.element(inici,0,[inici]))
        while queue._queue[-1]!=desti:
            node_imp = queue.pop()
            #print([x.pos for x in node_imp.track])
            if (sum([p in [x.pos if type(x)!=tuple else x for x in node_imp.track] for p in set(visits1)]))+1 == len(set(visits1)):
                to_visit = [p for p in set(visits1) if p not in node_imp.track][0]
                node_imp.track+=self.get_path(node_imp.elem,to_visit)
                
            if (sum([p in [x.pos if type(x)!=tuple else x for x in node_imp.track]for p in set(visits1)])) == len(set(visits1)):
                if node_imp.track[-1]!=desti:
                    if desti in self.nodes[node_imp.track[-1]]:
                        node_imp.track.append(desti)
                    else:
                        nodeact=node_imp.track[-1]
                        return [x.pos if type(x)!=tuple else x for x in node_imp.track] + self.get_path(nodeact,desti)[1:]

            if all([y in node_imp.track for y in visits1]) and node_imp.track[-1] == desti:
                return [x if type(x)==tuple else x.pos for x in node_imp.track]


            queue = self.ramifica(node_imp,queue,visits1)
            
            
    def cycles(self,trac):
        if len(trac)<4:
            return False
        for x in range(len(trac)-4):
            if trac[x] == trac[x+2] == trac[x+4]:
                return True
        return False
    
    def count_reps(self,track):
        n=0
        for x in track:
            for y in track:
                 if x==y :
                    n+=1
        return n - len(track)
    
    def calc_distance(self,track):
        sum=0
        for x in range(len(track)-1):
            sum+= (track[x].pos[0] -track[x+1].pos[0])**2 + (track[x].pos[1]-track[x+1].pos[1])**2
        return sum
    
    def ramifica_B_2(self,node, queue, visit,desti,bound):
        from_source = self.dijkstra(node.elem)
        indexes_v = [x for x, y in enumerate(self.nodes) if y in visit]
        for y in self.nodes[node.elem]:

                inici = [(x,y) for x, y in enumerate(self.nodes) if node.elem == y][0]
                dijk_inici = self.dijkstra(inici[1])
                to_visits = [x for x in visit if x not in node.track+[y]]
                indexes_to_visit = [x for x,y in enumerate(self.nodes) if y in to_visits]
                d2 = [x.pos for x in self.nodes[y]]
                d3 = functools.reduce(operator.add, [list(self.nodes[x].keys()) for x in d2])
                if  (y in visit or any([p in d2 for p in visit]) or any([p in d3 for p in visit]) ) and not self.cycles(node.track + [y]) :
                        queue1 = copy.deepcopy(queue._queue)
                        for x in queue1:
                            if x.val> (((sum([dijk_inici[x] for x in indexes_to_visit]))+self.calc_distance(node.track+[y]))):
                                queue._queue= [s for s in queue._queue if x!=s]

                        el = self.element(y,((sum([dijk_inici[x] for x in indexes_to_visit]))+self.calc_distance(node.track+[y]))/(len(indexes_v)-len(indexes_to_visit))  , node.track+[y])
                        queue.append(el)
                #else:queue.append(self.element(y, node.val + dist, node.track + [y]))
        return queue,bound
    
    def B_B2(self,inici,desti,visits1):
        nodes = [(x, y) for x, y in enumerate(self.nodes)]
        queue = self.queue()
        inici = [x for x in nodes if x[1] == inici][0][1]
        queue.append(self.element(inici, 0, [inici]))
        indexes_to_visit = [x for x,y in enumerate(self.nodes) if y in visits1]
        dijk_inici = self.dijkstra(inici)
        bound =  sum([dijk_inici[x] for x in indexes_to_visit])*10
        while queue._queue[-1] != desti:
            node_imp = queue.pop()


            if (sum([p in [x.pos if type(x) != tuple else x for x in node_imp.track] for p in set(visits1)])) + 1 == len(set(visits1)):
                to_visit = [p for p in set(visits1) if p not in node_imp.track][0]
                node_imp.track += self.get_path(node_imp.elem, to_visit)
            if (sum([p in [x.pos if type(x) != tuple else x for x in node_imp.track] for p in set(visits1)])) == len(
                    set(visits1)):
                if node_imp.track[-1] != desti:
                    if desti in self.nodes[node_imp.track[-1]]:
                        node_imp.track.append(desti)
                    else:

                        nodeact = node_imp.track[-1]

                        return [x.pos if type(x) != tuple else x for x in node_imp.track] + self.get_path(nodeact,
                                                                                                          desti)[1:]
            # print(node_imp.track7)
            if all([y in node_imp.track for y in visits1]) and node_imp.track[-1] == desti:
                return [x if type(x) == tuple else x.pos for x in node_imp.track]

            queue,bound = self.ramifica_B_2(node_imp, queue, visits1,desti,bound)
            
    def read_txt(self, graph):
        with open(graph, 'r') as hdler:
            for x in hdler.readlines()[1:]:
                a, b, c, d = x.split()
                node1, node2 = (float(a), float(b)), (float(c), float(d))
                if node1 not in self.positions: self.positions[node1] = self.counter_nodes; self.counter_nodes += 1
                if node2 not in self.positions: self.positions[node2] = self.counter_nodes; self.counter_nodes += 1
                self.set_edge((node1, node2))
                
    def __del__(self):
        self.positions = {}
        self.nodes = {}
        
    def __repr__(self):
        return str({k.pos: {t.pos: self.nodes[k][t].distance for t in self.nodes[k]} for k in self.nodes})


'''a = Graph(file=path)

#print([x.pos for x in a.nodes])
node1 = [x.pos for x in a.nodes if x.pos == (14456,15189)][0]
node2 = [x.pos for x in a.nodes if x.pos == (14456,15189)][0]
visits = open(f'Tests_v1/Visits4.txt', 'r')
visits = [(float(x.strip().split()[0]), float(x.strip().split()[1])) for x in visits.readlines()[1:]]
print(a.B_B1(node1,node2,visits1=visits))
'''
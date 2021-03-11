# -*- coding: utf-8 -*-
"""
Created on Wen Mar  4 12:00:03 2020

@author: pol
"""


# This class represent a graph
class Graph:

    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = {}
        self.directed = directed

    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance

    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

# This class represent a node
class Node:

    # Initialize the class
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))

# Best-first search
def best_first_search(graph, heuristics, start, end):
    assert start in graph.graph_dict.keys(), "No existeix el node inicial al graf"

    inici = []
    final = []

    node_inicial = Node(start, None)
    node_final = Node(end, None)

    node_inicial.f = heuristics[start]
    inici.append(node_inicial)

    while len(inici) > 0:


        inici.sort()

        node_actual = inici.pop(0)

        final.append(node_actual)

        if node_actual == node_final:
            path = []
            while node_actual != node_inicial:
                path.append(node_actual.name + ': ' + str(node_actual.f))
                node_actual = node_actual.parent
            path.append(node_inicial.name + ': ' + str(node_inicial.f))

            return path[::-1]


        veins = graph.get(node_actual.name)

        for key, value in veins.items():

            vei = Node(key, node_actual)

            vei.g = node_actual.g + graph.get(node_actual.name, vei.name)
            vei.h = heuristics.get(vei.name)
            vei.f = vei.g + vei.h

            inici.append(vei)
    return None

# The main entry point for this module
def main():

    # Create a graph
    graph = Graph()

    # Create graph connections (Actual distance)
    graph.connect('A', 'B', 4)
    graph.connect('A', 'C', 3)
    graph.connect('B', 'F', 5)
    graph.connect('B', 'E', 12)
    graph.connect('C', 'D', 7)
    graph.connect('C', 'E', 10)
    graph.connect('D', 'E', 2)
    graph.connect('F', 'Z', 16)
    graph.connect('E', 'Z', 5)


    # Create heuristics (straight-line distance, air-travel distance)
    heuristics = {}
    heuristics['A'] = 14
    heuristics['B'] = 12
    heuristics['C'] = 11
    heuristics['D'] = 6
    heuristics['E'] = 4
    heuristics['F'] = 11
    heuristics['Z'] = 0


    # Run search algorithm
    path = best_first_search(graph, heuristics, 'A', 'Z')
    print(path)
    print()

# Tell python to run main method
if __name__ == "__main__": main()

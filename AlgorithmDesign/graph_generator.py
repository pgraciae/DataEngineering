#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:02:33 2020

@author: pol
"""

import networkx as nx
import random

def graph_generator(filename, num_nodes, p):
    G = nx.generators.fast_gnp_random_graph(num_nodes, p)
    pos = [(random.randrange(1,17000), random.randrange(1,17000)) for x in range(len(G.nodes()))]
    visits = [pos[random.randint(0,len(G.nodes()) - 1)] for i in range(int(0.1 * len(G.nodes())) if int(0.05 * len(G.nodes())) > 0 else 1)]
    with open('Grafo' + filename + '.txt', 'w') as file:
        file.write('Grafo\n')
        for edge in G.edges:
            file.write(str(str(pos[edge[0]][0]) + ' ' +  str(pos[edge[0]][1]) + ' ' + str(pos[edge[1]][0]) + ' ' + str(pos[edge[1]][1]) + '\n'))
    with open('Visits' + filename + '.txt', 'w') as file:
        file.write('Visits\n')
        for el in visits:
            file.write(str(str(el[0]) + ' ' + str(el[1]) + '\n'))
            
graph_generator('6', 20, 0.3)
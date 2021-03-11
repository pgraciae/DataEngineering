"""
editor: SublimeText

@author: Pol Gràcia Espelt

1533358
"""


g = {'a': [('p',4), ('j',15), ('b',1)],
            'b': [('a',1), ('d',2), ('e',2), ('c',2)],
            'j': [('a',15),('c',6)],
            'p': [('a',4),('d',8)],
            'd': [('b',2), ('g',3),('p',8)],
            'e': [('b',2), ('g',9), ('f',5), ('c',2),('h',4)],
            'c': [('b',2), ('e',2), ('f',5), ('i',20),('j',6)],
            'g': [('d',3), ('e',9), ('h',1)],
            'f': [('h',10), ('e',5), ('c',5),('i',2)],
            'i': [('c',20),('f',2)],
            'h': [('g',1),('e',4),('f',10)] 
        }



def prim(grafo,start):
    MST = [start]
    posibles = list(grafo.keys())
    posibles.remove(start)
    futuros = [grafo[start]]
    coste = 0
    while len(posibles) != 0:
        min_dist = float("Inf")
        for lista in futuros:
            for tupla in lista:
                if tupla[1] < min_dist and tupla[0] not in MST:
                    min_dist = tupla[1]
                    tupla_min = tupla

        posibles.remove(tupla_min[0])
        MST.append(tupla_min[0])
        futuros.append(grafo[tupla_min[0]])
        coste += min_dist
        start = tupla_min[0]

    return MST,coste


def ordenar_values(grafo):
    lista_ordenada = []
    for lista in grafo.values():
        for bucket in lista:
            lista_ordenada.append(bucket[1])
    lista = list(set(lista_ordenada))
    x = sorted(lista)
    return x

def rename_team(team, t1, t2):
    for k, v in team.items():
        if v == t1 or v == t2:
            team[k] = t2
    return team

def kruskal(grafo):

    MST = []
    coste = 0
    peso = ordenar_values(grafo)
    team = {k:n for n,k in enumerate(grafo.keys())}
    for p in peso:
        for node, aresta in grafo.items():
            for bucket in aresta:
                if bucket[1] == p and team[bucket[0]] != team[node]:
                    team = rename_team(team, team[bucket[0]], team[node])
                    if node not in MST:
                        MST.append(node)
                    if bucket[0] not in MST:
                        MST.append(bucket[0])
                    coste += bucket[1]
    return MST, coste


if __name__ == '__main__':
    mst, cost = prim(g, 'a')
    print('Prim:', mst ,' cost:', cost)
    k, c = kruskal(g)
    print('Kruskal:',k, 'cost:', c)

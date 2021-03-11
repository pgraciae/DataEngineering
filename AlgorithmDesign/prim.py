"""
editor: SublimeText

@author: Pol Gràcia Espelt

1533358
"""

def prim(grafo,start):
    MST = [start]
    posibles = grafo.keys()
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
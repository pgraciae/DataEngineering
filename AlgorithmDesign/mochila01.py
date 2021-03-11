# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:37:03 2020

@author: jbern
"""

class Item:
    peso = 0
    beneficio = 0
    ratio = 0
    def __init__(self, peso,beneficio):
        self.peso = peso
        self.beneficio = beneficio
        self.ratio = beneficio/peso
    def __comp__(self,item_b):
        if self.ratio > item_b.ratio:
            return True
        else:
            return False
    def __str__(self):
        return "Beneficio: "+str(self.beneficio)+" Peso: "+str(self.peso)+" Ratio: "+str(self.ratio)
            
    
class Nodo:
    nivel = 0;
    beneficio_camino = 0;
    limite_beneficio = 0;
    peso = 0;
    def __init__(self):
        self.nivel = 0
        self.peso = 0
        self.beneficio_camino = 0
        self.limite_beneficio = 0

def bound(node_u,n,W,items):
    if node_u.peso>=W:
        return 0
    
    beneficio_bound = node_u.beneficio_camino
    
    j = node_u.nivel + 1
    
    total_peso = node_u.peso
    
    while j<n and (total_peso + items[j].peso) <= W:
        total_peso = total_peso + items[j].peso
        beneficio_bound = beneficio_bound + items[j].beneficio
        j = j+1
        
    if j<n:
        beneficio_bound = beneficio_bound + (W-total_peso)*items[j].ratio
        
    return beneficio_bound

def ordenar(items,n):
    min = 0
    i_min = 0
    if n<len(items)-1:
        for i in range(n,len(items)-1):
            if items[i].ratio > min:
                i_min = i
                min = items[i].ratio
        temp = items[i_min]
        items[i_min] = items[n]
        items[n] = temp
        ordenar(items,n+1)
    
class Cola:
    def __init__(self):
        self.items=[]
    def add(self, x):
        self.items.append(x)
    def top_pop(self):
        try:
            temp = self.items[0];
            self.items.pop(0)
            return temp
        except:
            raise ValueError("La cola está vacía")
    def es_vacia(self):
        return self.items == []

def mochila(W,items,n):
    
  
    ordenar(items,0)
    
    cola = Cola()
    u = Nodo()
    v = Nodo()
    
    u.nivel = -1
    cola.add(u)
    
    max_beneficio = 0
    while cola.es_vacia() == False:
        
        u = cola.top_pop()
        
        if u.nivel == -1:
            v.nivel = 0
        elif u.nivel != n-1:
            v.nivel = u.nivel+1
            
        
         # No meto elemento en mochila
        
        v.peso = u.peso
        v.beneficio_camino = u.beneficio_camino
        v.limite_beneficio = bound(v,n,W,items)
        
        if v.limite_beneficio > max_beneficio:
            cola.add(v)
        
        # Meto elemento en mochila
        
        v.peso = u.peso + items[v.nivel].peso
        v.beneficio_camino = u.beneficio_camino + items[v.nivel].beneficio
        
        if v.peso <= W and v.beneficio_camino > max_beneficio:
            max_beneficio = v.beneficio_camino
            
        v.limite_beneficio = bound(v,n,W,items)
        
        if v.limite_beneficio > max_beneficio:
            cola.add(v)
        
        
    return max_beneficio
    
#items = [Item(2,40),Item(3.14,50),Item(1.98,100),Item(5,95),Item(3,30)]
#W = 10
#n = 5
    
items = [Item(2,10),Item(4,10),Item(6,12),Item(9,18)]
W = 15
n = 4
print(mochila(W,items,n))



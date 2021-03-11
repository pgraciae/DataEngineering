"""
Created on Mon May 4 19:08:00 2020

@author: pol 1533358
"""
import numpy as np 
import copy as cp


def Brunch():

	taula = np.array([[11,12,18,40],[14,15,13,22],[11,17,19,23],[17,14,20,28]])
	
	cota_max = np.trace(taula)
	cota_min = np.sum(np.min(taula,axis=0))
	
	tree = [[i] for i in taula[0]]
	min_val = cota_max
	
	while len(tree) != 0:	
		estimacions = aprox(tree,taula)
		tree,node = podar(estimacions,tree,cota_max)	
		expandeix(tree,node,taula)
		
		for i in tree:
			if len(i) == 4:
				if sum(i) < min_val:
					sol = i
					min_val = sum(i)
				tree.remove(i)	
	print("El camí mínimi és ",sol,"amb un cost de ",min_val)
	
def aprox(tree,taula):
	sumas = []
	for i in range(len(tree)):
		copia = cp.copy(taula)
		copia = filter(i,tree,copia)
		suma = sum(tree[i])
		for row in range(len(tree[i]),len(copia)):
			mi = np.min(copia[row])
			copia = np.delete(copia,np.where(copia[row] == mi),axis=1)
			suma+=mi
		sumas.append(suma)

	return sumas

def filter(index,tree,taula):
	bucket = tree[index]
	for i in bucket:
		taula = np.delete(taula,np.where(taula == i)[1],axis=1)
	return taula
	
def podar(estimacions,tree,cota_max):
	return [j for i,j in zip(estimacions,tree) if i < cota_max],tree[estimacions.index(min(estimacions))]


def expandeix(tree,node,taula):
	index = [np.where(taula[i] == node[i]) for i in range(len(node)) ]	
	for i in taula[len(node)]:
		if np.argwhere(taula[len(node)] == i) != tree.index(node) and np.argwhere(taula[len(node)] == i) not in index:
			tree.append(node+[i])
	tree.remove(node)
		
		
if __name__ == "__main__":

	Brunch()
	
			
				
	
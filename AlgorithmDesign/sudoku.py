# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 10:16:38 2020

@author: jbern
"""

from time import time


def correcte(taulell,num,posicio):
	x,y = posicio[0],posicio[1]
	#files
	for i in range(len(taulell[0])):
		if taulell[x][i] == num and y != i:

			return False
	

	#columnes
	for i in range(len(taulell)):
		if taulell[i][y] == num and x != i:
			return False

	
	#blocs
	blocx = x//3
	blocy = y//3

	for i in range(blocx*3,blocx*3 + 3):
		for j in range(blocy*3,blocy*3 +3):
			if taulell[i][j] == num and (i,j) != posicio:
				return False
	return True	

def soluciona(taulell):
	troba = troba_vuit(taulell)
	if not troba:
		return True
	else:
		F,C = troba

	for i in range(1,10):
		if correcte(taulell,i,(F,C)):
			taulell[F][C] = i
			if soluciona(taulell):
				return True
			taulell[F][C] = 0

	return False

def troba_vuit(taulell):
	for i in range(len(taulell)):
		for j in range(len(taulell[0])):
			if taulell[i][j] == 0:
				return(i,j)
	return False



def print_taulell(taulell):
	for i in range(len(taulell)):
		if i%3 == 0 and i !=0:
			print("------------------------------- ")
		

		for j in range(len(taulell[0])):
			if j%3 == 0 and j != 0:
				print(" | ",end = "")

			if j == 8:
				print(taulell[i][j])
			else:
				print(str(taulell[i][j]) + " ", end = " ")


if __name__ == '__main__':

	taulell=[[0,8,0, 0,0,2, 0,3,0],
	         [0,4,0, 1,3,0, 0,2,0],
	         [0,0,0, 7,0,0, 0,0,9],
	         [0,0,0, 8,0,0, 6,5,3],
	         [0,2,0, 0,4,5, 0,0,8],
	         [5,6,0, 0,0,3, 2,4,0],
	         [4,0,0, 0,0,0, 5,0,7],
	         [7,0,2, 0,0,0, 0,8,4],
	         [0,0,0, 4,0,0, 0,0,2]]

	print_taulell(taulell)

	start_time = time()
	soluciona(taulell)

	print("\n-------------------------------------\n")
	print_taulell(taulell)



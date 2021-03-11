import operator
import math
import random

class City:
    """A city with a name and 2D coordinates"""
    def __init__(self, city_name='NoName', posx=0, posy=0):
        self.name = city_name
        self.x = posx
        self.y = posy

def distance_between_cities( C1, C2 ):
    """Compute distance between two cities"""
    
    return math.sqrt( (C1.x-C2.x)*(C1.x-C2.x) + (C1.y-C2.y)*(C1.y-C2.y))

def create_random_cities ( N, filename ):
    """Create a file containing N randomly-generated cities"""
    with open(filename, 'w') as file:
        for i in range(N):
            file.write( "A"+str(i)+" "+
                        str(random.random()*1000)+" "+
                        str(random.random()*1000)+"\n" )

def read_cities_from_file ( filename ):
    """Read list of Cities from text file"""
    Cities= [] # List of Empty Cities
    with open(filename) as file:
        for line in file:
            R= line.split()
            Cities.append ( City( R[0], float(R[1]), float(R[2]) ) )
    return Cities

def path_distance( Cities ):
    """Compute total distance of the path traversing all cities in order"""
    D = 0
    for i in range( len(Cities) ):
        D = D + distance_between_cities ( Cities[i],
                                          Cities[i+1 if i+1<len(Cities) else 0])
    return D

def closerCity( City, ordx, indexx, ordy, indexy ):
    """Compute position of the city C in the list of Cities that is closer to City"""
    #definim els valors que dins la nostra llista ordenada queden més aprop del valor de x i y
    apropx = ordx[indexx - 120 if indexx - 120 >= 0 else 0 : \
    			indexx + 120 if indexx + 120 <= len(ordx) else len(ordx) ]

    apropy = ordy[indexy - 120 if indexy - 120 >= 0 else 0 : \
    			indexy + 120 if indexy + 120 <= len(ordy) else len(ordy) ]

    #prenem el valor que queda mes aprop en la distància euclidia que ja esta aprop de x o y.
    distances = min([ (distance_between_cities( City, c ),c) for c in apropx] +\
    			 [(distance_between_cities(City, c), c) for c in apropy])
    
    return distances[1]

def GoodPath( Cities ):
    """Generate a path with small total distance using greedy algorithm"""
    #ordenat x
    ordx = sorted(Cities, key = operator.attrgetter("x"))
    #ordenat y 
    ordy = sorted(Cities, key = operator.attrgetter("y"))
    #definim els valors inicials. Farem el path i el ordy en funcio de les variacions de la llista de x
    Path = [Cities[0]]
    indexx = ordx.index(Cities[0])
    indexy = ordy.index(Cities[0])
    del ordy[indexy]
    del ordx[indexx]

    #fem una variable index de x i y per poder posteriorment accedir al valor de la llista ordenada\
    # on li correspondria estar al valor que hem eliminat

    while len(ordx) > 0:	
        ciutat = closerCity( Path[-1], ordx, indexx, ordy, indexy )
        pos = ordx.index(ciutat)
        Path.append( ordx[pos] ) 
        indexx = pos
        indexy = ordy.index(ordx[pos])
        del ordy[indexy]
        del ordx[indexx]

    return Path

if __name__ == "__main__":
  import argparse as arg
  parser = arg.ArgumentParser(prog='ARGUMENTS', usage='%(prog)s [options]')
  parser.add_argument("input",  type=str, help="File containing list of Cities")
  args = parser.parse_args()

  ListOfCities= read_cities_from_file ( str(args.input) )
  GoodList    = GoodPath( ListOfCities )
  print ( "Initial Distance =", path_distance( ListOfCities ),
          "  Good Distance =",  path_distance( GoodList) )





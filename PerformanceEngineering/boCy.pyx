import math
import random
import cython

class City:
    """A city with a name and 2D coordinates"""
    def __init__(self, city_name='NoName', posx=0, posy=0):
        self.name = city_name
        self.x = posx
        self.y = posy

def distance_between_cities( C1, C2 ):
    """Compute distance between two cities"""
    dx = C1.x - C2.x
    dy = C1.y - C2.y
    return math.sqrt( dx*dx + dy*dy )

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


cdef int closerCity( float x, float y, int N, float [::1] Cx, float [::1] Cy ):
    """Compute position of the city C in the list of Cities that is closer to City"""
    cdef float dx, dy, dist, minDist = 2*1000*1000
    cdef int   i, minIndex= 0
    for i in range(N):
        dx, dy = x - Cx[i], y - Cy[i]
        dist   = dx*dx + dy*dy
        if dist < minDist:
            minDist, minIndex = dist, i
    return minIndex

def GoodPath( Cities ):
    """Generate a path with small total distance using greedy algorithm"""
    import numpy as np
    cdef float[::1] Cx, Cy
    cdef float x, y
    cdef int   pos, N
    cdef object City
    NotVisited = [i for i in Cities]
    Path= [ Cities[0] ]
    del NotVisited[0]
    N = len(NotVisited)
    Cx = np.array([c.x for c in NotVisited], dtype=np.float32) 
    Cy = np.array([c.y for c in NotVisited], dtype=np.float32)
    while N > 0:
        City = Path[-1]
        x, y = City.x, City.y
        pos = closerCity( x, y, N, Cx[0:N], Cy[0:N] )
        Path.append( NotVisited[pos] )        
        NotVisited[N-1], NotVisited[pos] = NotVisited[pos], NotVisited[N-1]
        Cx[N-1], Cx[pos] = Cx[pos], Cx[N-1]
        Cy[N-1], Cy[pos] = Cy[pos], Cy[N-1]
        N = N-1

    return Path




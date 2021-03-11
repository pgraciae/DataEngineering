# This code implements the simulation of the movement of a string
# using the numerical method of finite differences

import math
import cython
from cpython cimport array
import array
import numpy as np
cimport numpy as np

@cython.boundscheck(False)
cpdef void run( int X, int T ):

  cdef array.array  t0 = array.array('f', [0]*(X + 1))#array.array ('f', [0] * (X + 1))
  cdef array.array  t1 = array.array('f', [0]*(X + 1))
  cdef float L = 0.345678
  cdef array.array  t2 = array.array('f', [0]*(X + 1))
  #cdef float[:] t2 = t20
  #print("String motion: X=", X, " and T= ", T)

  # initialize positions of matrix U
  cdef int x, t, z
  cdef float S

  for x in range (1,X):
    t0[x] = math.sin( x * math.pi / X )
    t1[x] = t0[x] * math.cos( math.pi / (T+1) )
  
  # compute simulation
  cdef float op = 2 * (1 - L)
  for t in range(T):
    for z in range(1,X):
      t2[z] = t1[z] * op + (t1[z+1] + t1[z-1]) * L - t0[z]
    
    #t2 = t1 + tmp - t0 
    t0 = t1
    t1 = t2


  # compute checksum
  S= 0
  for x in range(1,X):
    S += t1[x]

  print("CheckSum = ", S)

"""
if __name__ == "__main__":
  import argparse as arg
  parser = arg.ArgumentParser(prog='ARGUMENTS', usage='%(prog)s [options]')
  parser.add_argument("X",  type=int, help="X and T")
  parser.add_argument("T",  type=int, help="X and T")

  args = parser.parse_args()

  run(args.X, args.T)
"""
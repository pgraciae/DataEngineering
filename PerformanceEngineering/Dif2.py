import numpy as np
cimport numpy as np

##tenint en compte que el shape l'agafem des del grip que es l'unic valor que passem per defecte

cpdef run_experiment(unsigned int num_iterations,   int D = 1,  float dt = 0.1):
  # Setting up initial conditions
  cdef int xmax = 1024
  cdef int ymax = 1024
  cdef int mul = 1024*1024
  cdef int i,j,n

  cdef np.ndarray[float, ndim=2] grid = np.zeros(xmax*ymax, dtype = np.float32).reshape((xmax,ymax))
  
  for i in range(xmax):
    for j in range(ymax):
      grid[i][j] = (i * j) / (mul)

  cdef np.ndarray[float, ndim=2] grid_xx
  cdef np.ndarray[float, ndim=2] grid_yy


  for i in range(num_iterations):
    #He averiguat que és milesimes de segon més rapid modificant directament les columnes amb stack fent servir indexacions de matrius que fent servir el roll
    grid_yy = np.column_stack((grid[:,1:], grid[:,0])) + np.column_stack((grid[:,-1], grid[:,:-1]))
    grid_xx = np.vstack((grid[1:,:], grid[0,:])) + np.vstack((grid[-1,:], grid[:-1,:]))
    grid += D * ((grid_yy + grid_xx) - 4*grid) * dt

  return np.sum(grid)
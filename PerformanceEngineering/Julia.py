# area of complex space to investigate
import numpy as np
cimport cython

cdef float x1 = -1.8
cdef float x2 = 1.8
cdef float y1 = -1.8
cdef float y2 = 1.8
cdef float c_real = -0.62772
cdef float c_imag = -.42193

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.initializedcheck(False) 

cpdef calc_pure_python( desired_width, max_iterations):
  """Create a list of complex coordinates (zs) and complex parameters (cs), build Julia set, and display"""

  cdef float x_step = (float(x2 - x1) / float(desired_width))
  cdef float y_step = (float(y1 - y2) / float(desired_width))
  
  x = np.arange(x1,x2,x_step, dtype = float)
  y = np.arange(y2,y1,y_step, dtype = float)

  # Build a list of coordinates and the initial condition for each cell.
  # Note that our initial condition is a constant and could easily be removed;
  # we use it to simulate a real-world scenario with several inputs to
  # our function.
  zs = []

  for ycoord in y:
    for xcoord in x:
      zs.append(complex(xcoord, ycoord))

  cs = np.full((len(zs)), complex(c_real,c_imag))
  output = calculate_z(max_iterations, zs, cs)


  # This sum is expected for a 1000^2 grid with 300 iterations.
  # It catches minor errors we might introduce when we're
  # working on a fixed set of inputs.
  #assert sum(output) == 33219980
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.initializedcheck(False) 

cpdef calculate_z( unsigned int maxiter, zs, double complex[:] cs):
  """Calculate output list using Julia update rule"""
  output = np.empty(len(zs))
  cdef unsigned int i,n 
  cdef double complex z,c
  for i in range(len(zs)):
    n = 0
    z = zs[i]
    c = cs[i]
    while  n < maxiter and(z.real * z.real) + (z.imag * z.imag) < 4:
      z = z * z + c
      n += 1
    output[i] = n
  return output

if __name__ == "__main__":
  # Calculate the Julia set using a pure Python solution
  calc_pure_python(desired_width=1000, max_iterations=300)




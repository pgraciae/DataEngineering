#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* compilar:
	gcc -fPIC -shared -fopenmp -std=c99 -o func.so func.c
*/


float stencil (float v1, float v2, float v3, float v4)
{
  return (v1 + v2 + v3 + v4) * 0.25f;
}


float max_error ( float prev_error, float old, float new )
{
  float t= fabsf( new - old );
  return t>prev_error? t: prev_error;
}


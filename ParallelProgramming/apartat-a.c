#include <omp.h>
#include <stdio.h>

void par_func(){
	#pragma omp parallel num_threads(2)
	{
	printf("PAR_FUNC: Thread %d des de la secció paral·lela\n", omp_get_thread_num());
	}
}

int main(){
	#pragma omp parallel num_threads(2)
	{
	omp_set_nested(1);
	printf("MAIN: thread %d des de la secció paral·lela\n", omp_get_thread_num());
	par_func();
	}
}



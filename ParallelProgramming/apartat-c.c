#include <omp.h>
#include <stdio.h>



/*
int x = 10;
int main(){ //Arxiu apartat-c_1.c
	#pragma omp parallel num_threads(8)
	{
	x = omp_get_thread_num();
	}
	printf("X = %d\n", x);
}
*/

int x = 10;

int main(){
	#pragma omp parallel num_threads(8) private(x)
	{
		x += omp_get_thread_num();
		printf("X = %d\n", x);
	}
}




#include <omp.h>
#include <stdio.h>

int main(){
	#pragma omp parallel for num_threads(3)
		for (int i = 0; i < 4; ++i) {
			for (int j = 0; j < 4; ++j) {
				printf("Thread %d i= %d, j= %d\n",omp_get_thread_num(),i,j);
			}
		}
	}
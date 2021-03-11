#include<stdio.h>
#include<mpi.h>


int main(int argc, char *argv[]){

	int my_rank, nprocs;
	MPI_Status status;
	MPI_Init( &argc, &argv);
	MPI_Comm_rank( MPI_COMM_WORLD, &my_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
	printf("nprocss: %d\n", nprocs);
	int part = 10000;
	int N = part / nprocs;
	int sum[nprocs], i, numero = 0;

	switch (my_rank) {
		case 0:
			printf("%d\n", 0);
			for (i = 0; i < N ; i++){
				sum[my_rank] += i;
			}
			for ( int j = 1; j < nprocs; j++){
				MPI_Recv(&sum[j], 1, MPI_INT, j , 0, MPI_COMM_WORLD, &status );
				sum[0] += sum[j];
			}
			printf("El número és: %d\n", sum[0]);
			return sum[0];

		case 1:
			for (i = my_rank * N; i < N * (my_rank + 1) ; i++){
				sum[my_rank] += i;
			}
			MPI_Send(&sum[my_rank], 1, MPI_INT, 0 , 1, MPI_COMM_WORLD );

		case 2:
			for (i = my_rank * N; i < N * (my_rank + 1) ; i++){
				sum[my_rank] += i;
			}
			MPI_Send(&sum[my_rank], 1, MPI_INT, 0 , 2, MPI_COMM_WORLD );
		case 3:
			for (i = my_rank * N; i < N * (my_rank + 1) ; i++){
				sum[my_rank] += i;
			}
			MPI_Send(&sum[my_rank], 1, MPI_INT, 0 , 3, MPI_COMM_WORLD );
	}
	
	MPI_Finalize();

}

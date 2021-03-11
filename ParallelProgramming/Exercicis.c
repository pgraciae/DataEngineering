 #include <stdio.h>
#include <mpi.h>

#define N 100

//Funció per inicialitzar les matrius
void init_data(float A[N][N], float B[N][N], float C[N][N])
{
        for(int i=0; i < N; i++)
                for(int j=0; j < N; j++){
                        A[i][j] = 1.0; B[i][j] = 1.0*j; C[i][j] = 0.0;
                }
}

//Aquí es fa la multiplicació C=AxB (o part de la multiplicació)
void multiplica(float A[N][N], float B[N][N], float C[N][N], int M)
{
	for( int i = 0; i < M; i++)
		for( int j = 0; j < N; j++ )
			for (int z = 0; z < N; z++ ) C[i][j] += A[i][z] * B[j][z];
}

//Revisem que el resultat sigui correcte
void check_results( float C[N][N] ){
        for(int i = 0; i < N; i++)
                for(int j = 0; j < N; j++)
                        if ( C[i][j] != (N*(N-1))/2.0 ){
                                printf("Error!! C[%d][%d] = %f != %f\n", i, j, C[i][j], (N*(N-1))/2.0);
                                return;
                        }
        printf("Tot correcte C[i][j] = %f per tota la matriu\n", C[0][0] );
}

int main( int argc, char *argv[] )
{
	float A[N][N], B[N][N], C[N][N];
	int my_rank, nprocs;
	MPI_Status status;

	MPI_Init( &argc, &argv );
	MPI_Comm_rank( MPI_COMM_WORLD, &my_rank);
	MPI_Comm_size( MPI_COMM_WORLD, &nprocs);

	//El procés amb rank 0 inicialitza i envia les dades. B a tots els processos, A repartida per files 
	if (my_rank == 0){ 
		init_data( A, B, C );
		int residu = N % nprocs;
		for(int i = 1; i < nprocs; i++){
			MPI_Send(B, N*N, MPI_FLOAT, i, 0, MPI_COMM_WORLD );
			for(int j=0; j < N/nprocs; j++)
				MPI_Send(A[i*(N/nprocs)+j], N, MPI_FLOAT, i, 0, MPI_COMM_WORLD);
		}
		// la nostra i = nprocs -1 
		if(residu != 0){
			for(int k = 0; k < residu; k++){
					MPI_Send(A[N + k], N, MPI_FLOAT, k, 0, MPI_COMM_WORLD);
				}
			}
		}  else {
	//Els processos amb rank diferent de 0 reben les dades. Tota la matriu B, la seva part d'A
		MPI_Recv(B, N*N, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, &status );
		for(int j=0; j < N/nprocs; j++){
                	MPI_Recv(A[j], N, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, &status );
        }
        if(residu != 0){
        	for(int k = 0; k < residu; k++){
        		if(my_rank == k){
        			MPI_Recv(A[j + 1], N, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, &status)
        		}
        	}

        }
	}
	
	//Tothom fa una part de la multiplicació   
	multiplica( A, B, C, N/nprocs);

	//El procés amb rank 0 rep les files de la matriu C que han estat calculades per la resta i
	//comprova que tot estigui bé (resultat correcte)
	if (my_rank == 0){
		for (int i = 1; i < nprocs; i++){
                        for(int j=0; j < N/nprocs; j++){
                                MPI_Recv(C[i*(N/nprocs) + j], N, MPI_FLOAT, i, 0, MPI_COMM_WORLD, &status );
                        }
        }
		check_results( C );
	} else {
		//Cada procés envia la part de la matriu resultat que ha calculat al procés 0
		for( int i=0; i < N/nprocs; i++ ){
			MPI_Send( C[i], N, MPI_FLOAT, 0, 0, MPI_COMM_WORLD );
		}
	}
	MPI_Finalize();

}

import numpy as np


def BinSearch(Val, Idx, Pos, N, M):
  for i in range(M):
    V = Val[i]
    Left =-1
    Right= N
    Size = (Right - Left) >> 1  # integer division by 2 implemented by bit shifting 
    while (Size > 0):
      Middle = Left + Size
      value  = Idx[Middle]
      if (value < V):
        Left = Middle
      else:
        Right= Middle
      Size = (Right - Left) >> 1 
    Pos[i] = Right



def run(N,M, rep):
  
  print("Generar N=", N, "y M=", M, "números aleatorios entre 0 y", N*10)
  np.random.seed(0)
  RndIndex  = np.random.rand ( N )
  Index     = np.empty ( N, dtype= np.int32 )
  RndValues = np.random.rand ( M )
  Values    = np.empty ( M, dtype= np.int32 )
  Positions = np.empty ( M, dtype= np.int32 )

  for i in range(N):
    Index[i] = (RndIndex[i]*N*10)  # scale and round to unsigned integer

  for i in range(M):
    Values[i]= (RndValues[i]*N*10)  # scale and round to unsigned integer

  print("Ordenar", N, "valores del array Index")
  Index = np.sort(Index)  # create a sorted copy of numpy array

  print("Buscar", rep, "veces", M, "valores del array Values[] en el array Index[]")
  for r in range(rep):
    BinSearch ( Values, Index, Positions, N, M)
    Values[r] += Positions[r] # artificial loop-carried dependence

  if (rep == 1):
    Values[0] -= Positions[0]  # correct previous modification
  Verify(Index, Values, Positions, N, M)


def Verify(Idx, Val, Pos, N, M):

  print("Verificar búsquedas y contar ocurrencias")
  Count = 0
  for i in range(M):
    p, v  = Pos[i], Val[i]
    if (p>0 and Idx[p-1] >= v):
      print("Error")
    while (p<N and Idx[p] == v):
      Count, p = Count+1, p+1
    if (p<N and Idx[p] < v):
      print("Error")

  print ("Se han encontrado", Count, "ocurrencias de Values[] en Index[]")

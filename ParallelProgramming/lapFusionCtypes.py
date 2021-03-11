import numpy as np
import sys
import ctypes
import multiprocessing as mp

func = ctypes.CDLL('./func.so')  #funció que conté les fucnions del executable de C

def laplace_step(entra,surt):
    for i in range(1,val-1): #iterem fins a la fila i columna que li pertoca
        for j in range(1,val-1): #iterem fins a la fila i columna que li pertoca
            surt[i][j] = func.stencil(entra[i-1][j], entra[i+1][j], entra[i][j-1], entra[i][j+1])  #cridem la funció de C
    return (np.absolute(surt-entra)).max() #prenem el valor més gran dels errors

def laplace_init(entra):  #inicialitzem els valors de les matrius
   for i in range(n): entra[i][0] = np.sin(np.pi*i/(n-1))
   for i in range(n): entra[i][-1] = entra[i][0]*np.exp(-np.pi)
   
def calcul_error(idx, val, A, temp, nump, local_errors):
    itera = 0  #inicialitzem el nombre d'iteracions a 0
    while (error.value < max(local_errors)) or (itera < max_iter): #condicions de parada
        my_error = laplace_step(A[idx*val:(idx+1)*val], temp[idx*val:(idx+1)*val])  #crida a la funció laplace on cada thread calculara la part que li correspon del laplace step
        swap = A[idx*val:(idx+1)*val] 
        A[idx*val:(idx+1)*val] = temp[idx*val:(idx+1)*val]   ##intercanviem els valors que corresponen a cada thread entre A i temp
        temp[idx*val:(idx+1)*val] = swap
        local_errors[idx] = my_error  #variable global 
        itera += 1    #incrementem el numero d'iteració

if __name__ == '__main__':
    tol = 1.0e-5
    
    global error  
    error = mp.Value('d', tol**2)  #fem una variable shared error
    itera = 0
    n = 4096 if len(sys.argv) <= 1 else int(sys.argv[1])
    max_iter = 1000 if len(sys.argv) <= 2 else int(sys.argv[2])
    
    global A  #A es una variable global però no compartida ja que sinó el procés és molt lent
    global temp #temp es una variable global però no compartida ja que sinó el procés és molt lent
    A = np.zeros([n,n])
    temp = np.zeros([n,n])
    
    laplace_init(A) #incialitzem A
    laplace_init(temp) #inicialitzem temp
    
    A[n//128][n//128] = 1.0
    
    print(f'Jacobi relaxation Calculation: {n}x{n} mesh, maximum of {max_iter} iterations')
    
    # Multiprocessing
    nump= mp.cpu_count() #num cpus
    val = n//nump  #càlcul de files d'A que li correspon a cada processador
    
    local_errors = mp.Array('d',[1.0]*nump)   #array de memoria compartida on cada thread calcularà el error corresponent i agafarem el valor màxim en cada iteració fins que es compleixin les condicions.
    procs = [mp.Process(target=calcul_error, args=(i, val, A, temp, nump, local_errors)) for i in range(0,nump)]  #inicialitzem els procesos
    
    for i in range(0, nump):   #comencem els procesos
        procs[i].start()
    for i in range(0, nump):   #finalitzem els procesos
        procs[i].join()
        
    print(f'Total Iterations: {itera}, ERROR: {error.value}')
    print(f'A[{n//128}][{n//128}]= {A[n//128][n//128]}')
    


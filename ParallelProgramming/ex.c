#include <omp.h>
#include<stdio.h>

int a,b;
#pragma omp threadprivate(b)
void main(){
a = 10;
#pragma omp parallel firstprivate(a)
{
printf("1. a %d, num %d\n",a, omp_get_thread_num()); // I
a = 10;
#pragma omp master
{
a = 25;
}
printf("2. a %d, num %d\n", a, omp_get_thread_num()); // II
}
b = 5;
#pragma omp parallel copyin(b)
{
#pragma omp master
{
b = 1;
}
printf("3. a %d b %d, num %d\n", a, b, omp_get_thread_num()); // III
}
printf("4. a %d b %d, num %d\n", a, b, omp_get_thread_num()); // IV
}

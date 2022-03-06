# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:44:50 2022

@author: pavmb
"""


from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
import random

NPROD = 3
N = 5


def productor(sem_empty,sem_nonempty,storage, idx):
    v = 0 
    for i in range(N):
        sleep(random.random()/3)
        v += random.randint(0,5)
        sem_empty[idx].acquire()# wait empty
        print (f"producer {current_process().name} produciendo")
        storage[idx] = v
        sem_nonempty[idx].release()  # signal nonEmpty
      
    v = -1
    sem_empty[idx].acquire()# wait empty
    storage[idx] = v
    print(f"producer {current_process().name} terminado")
    sem_nonempty[idx].release() # signal nonEmpty
    
    
    
def minimo(lista):
    aux=[]
    for i in range(len(lista)):
        aux.append(0)
    maximo = max(lista)
    for i in range(len(lista)):
        if lista[i] == -1:
            aux[i] = maximo + 1
        else:
            aux[i] = lista[i]
    minimo = aux[0]
    idx = 0
    for i in range(1, len(aux)):
        if aux[i] < minimo and aux[i] != -1:
            minimo = aux[i]
            idx = i
    return minimo, idx
    
    
def consumidor(sem_empty,sem_nonempty, storage):  
    
    numeros = []
    listacompleta=[]
    for i in range(NPROD):
        listacompleta.append(-1)
        
    for i in range(NPROD):
        sem_nonempty[i].acquire() # wait nonEmpty
        
    while listacompleta != list(storage):
        
        v, i = minimo(storage)
        print('se añade:', v, 'de Productor', i)
        sleep(random.random()/3)
        numeros.append(v)
        sem_empty[i].release() # signal empty
        print('consumiendo', v)
        sem_nonempty[i].acquire() # wait nonEmpty
    
    print('Todo consumido')
    print ('Almacen: ', numeros)




def main():
    storage = Array('i',NPROD)
    
    sem_empty=[]
    sem_nonempty=[]
    for i in range(0,NPROD):
        non_empty = Semaphore(0)
        empty = BoundedSemaphore(1)
        sem_empty.append(empty)
        sem_nonempty.append(non_empty)
    prodlst = [ Process(target = productor, 
                       name=f'prod_{i}', 
                       args=(sem_empty,sem_nonempty,storage,i))
                    for i in range (NPROD)]
    cons = Process(target = consumidor, args = (sem_empty,sem_nonempty,storage))
    
    
    for p in prodlst:
        p.start()
    cons.start()

    for p in prodlst:
        p.join()
    cons.join()



if __name__ == "__main__":
 main()    
           

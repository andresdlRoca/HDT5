import simpy
import random


#Env: Variable del enviroment de simpy
#ID: identificador del proceso
#cpu: Velocidad del cpu
#RAM: Capacidad de memoria total que tiene la simulacion
#Memoria: Cantidad de memoria que usara el proceso
#Delay: Simulacion de la llegada de procesos 
#contadorRAM: Variable int que lleva la cuenta de cuanta RAM hay disponible en el sistema.

def simulacion(env, ID, cpu, RAM, memoria, delay, contadorRAM):
  yield env.timeout(delay)
  countprint = 0

  with cpu.request() as req:
    #ready
    while(memoria > 0):
      RAM.get(memoria)
      yield req
      if(countprint < 1):
        print("%s llego en %d" % (ID, env.now))
      countprint += 1
      yield env.timeout(3)
      memoria = memoria - 3
      
    print("%s salio en %d" % (ID, env.now))
    

    
    


  


#
maxRAM = 200
env = simpy.Environment()
RAM = simpy.Container(env, init = maxRAM, capacity = maxRAM)
Velocidadcpu = simpy.Resource(env, capacity = 1)

#Creacion de los procesos
intervalo = 10
random.seed(10)
for i in range(25):
  memoriaProceso = random.randint(1, 10)
  env.process(simulacion(env, "Proceso %d" % i, Velocidadcpu, RAM, memoriaProceso, random.expovariate(1.0/intervalo), maxRAM))

#Correr la simulacion
env.run()

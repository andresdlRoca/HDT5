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
  global tiempoTotal
  global tiempoPromedio
  countprint = 0
  llegada = env.now
  tiempoTotal = 0
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
      
    tiempoTotal = env.now - llegada
    print("%s salio en %d" % (ID, env.now))
    tiempoPromedio = tiempoTotal/25


def running(env,ID,cpu,RAM,proceso,delay, contadorRAM):
  yield env.timeout(3)
  if(proceso == 1 ):
    proceso = proceso - 1
  if(proceso == 2 ):
    proceso = proceso - 2
  else:
    proceso = proceso - 2
  
  wait = random.randint(1, 2)
  if(wait == 1):
    env.process(Wait(env,ID,cpu,RAM,proceso,delay, contadorRAM))
  else:
    env.process(simulacion(env,ID,cpu,RAM,proceso,delay, contadorRAM))

def Wait(env,ID,cpu,RAM,proceso,delay, contadorRAM):
  yield env.timeout(3)
  env.process(simulacion(env,ID,cpu,RAM,proceso,delay, contadorRAM))
  


#
maxRAM = 200
env = simpy.Environment()
RAM = simpy.Container(env, init = maxRAM, capacity = maxRAM)
Velocidadcpu = simpy.Resource(env, capacity = 1)

#Creacion de los procesos
intervalo = 10
random.seed(10)
for i in range(25):
  #Asignacion de instrucciones
  memoriaProceso = random.randint(1, 10)

  if(memoriaProceso >= 1):
    env.process(running(env, "Proceso %d" % i, Velocidadcpu, RAM, memoriaProceso, random.expovariate(1.0/intervalo), maxRAM))  
  else:
    env.process(simulacion(env, "Proceso %d" % i, Velocidadcpu, RAM, memoriaProceso, random.expovariate(1.0/intervalo), maxRAM))


  

#Correr la simulacion
env.run()
print("El tiempo promedio de completacion " ,tiempoPromedio)
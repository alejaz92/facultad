import math
import os
import sys
import random
from matplotlib import pyplot as plt

# define las variables globales
Q_LIMIT = 100
BUSY = 1
IDLE = 0

next_event_type = 0
num_custs_delayed = 0
num_delays_required = 0
num_events = 0
num_in_q = 0
server_status = 0
area_num_in_q = 0.0
area_server_status = 0.0
mean_interarrival = 0.0
mean_service = 0.0
time = 0.0
time_arrival = [0]*(Q_LIMIT + 1)
time_last_event = []
time_next_event = [0]*3
total_of_delays = 0.0
delay = 0.0

arreglo_retraso_promedio = []
arreglo_cant_personas_cola = []
arreglo_utilizacion_servidor = []
arreglo_tiempo_total =[]

def main():
    global mean_service
    global mean_interarrival
    global num_delays_required
    global num_custs_delayed
    global num_events

    #Se establecen los parametros
    num_events = 2
    mean_interarrival = 1/1.75
    mean_service = 1/3
    num_delays_required = 1000

    initialize()

    f = open("mm1.txt", "a")
    f.write("\nParametros ingresados:")
    f.write("\nTiempo promedio entre arribos (en minutos): " + str(mean_interarrival))
    f.write("\nTiempo promedio de servicio (en minutos): " + str(mean_service))
    f.write("\nNumero de clientes " + str(num_delays_required))
    f.write("\n\nValor Lambda: " + str(1/mean_interarrival))
    f.write("\nValor Mu: " + str(1/mean_service))

    while num_custs_delayed < num_delays_required:
        timing()
        update_time_avg_stats()

        if(next_event_type == 1):
            arrive()
        else:
            depart()
    report()

def initialize():
    global time
    global server_status
    global num_in_q
    global time_last_event
    global num_custs_delayed
    global total_of_delays
    global area_num_in_q
    global area_server_status
    global time_next_event
    global mean_interarrival
    global delay

    #inicializar reloj
    time = 0

    #inicializar las variables de estado
    server_status = IDLE
    num_in_q = 0
    time_last_event = 0

    #inicializo los contadores estadisticos
    num_custs_delayed = 0
    total_of_delays = 0
    area_num_in_q = 0
    area_server_status = 0

    #inicializo lista de eventos
    time_next_event[1] = time + expon(mean_interarrival)
    time_next_event[2] = sys.maxsize

    #crea archivo de registro
    createFile()


def timing():
    global next_event_type
    global num_events
    global time_next_event
    global time

    min_time_next_event = 10**30 #por poner un numero exageradamente grande
    next_event_type = 0

    #determina el tipo del proximo evento
    for i in range(num_events):
        if (time_next_event[i+1] < min_time_next_event):
            min_time_next_event = time_next_event[i+1]
            next_event_type = i+1

    #chequea si la lista de eventos esta vacia
    if (next_event_type == 0):
        #la lista de eventos esta vacia, por lo tanto termino la simulacion
        print("Lista de eventos vacia en tiempo", time)
    #la lista de eventos no esta vacia por lo que adelanto el reloj
    time = min_time_next_event

def arrive():
    global time_next_event
    global time
    global mean_interarrival
    global server_status
    global BUSY
    global num_in_q
    global Q_LIMIT
    global total_of_delays
    global num_custs_delayed
    global delay

    #programa el siguiente arrivo
    time_next_event[1] = time + expon(mean_interarrival)

    #valida si el servidor esta ocupado, entonces incrementa el numero de clientes en cola
    if server_status == BUSY:
        #el servidor esta ocupado, entonces incrementa
        num_in_q += 1

        #valida si la cola supera el limite
        if(num_in_q == Q_LIMIT):
            f = open("mm1.txt", "a")
            f.write("\nSe supero el limite de la cola en el tiempo " + str(time))
            exit(2)
        #aun hay espacio en la cola, por lo tanto se guarda el tiempo de arrivo del ultimo cliente al final  del arreglo
        time_arrival[num_in_q] = time
    else:
        #el servidor está inactivo, por lo que el cliente que llega tiene un retraso de cero
        #(Las siguientes dos declaraciones son para la claridad del programa y no afectará los resultados de la simulación)
        delay = 0.0
        total_of_delays += delay

        #aumente el número de clientes retrasados ​​y hace que el servidor esté ocupado
        num_custs_delayed += 1
        server_status = BUSY

        #finalizacion del servicio
        time_next_event[2] = time + expon(mean_service)


def depart():
    global num_in_q
    global IDLE
    global server_status
    global time_next_event
    global time
    global time_arrival
    global num_custs_delayed
    global mean_service
    global total_of_delays
    global delay

    #Comprueba si la cola esta vacia
    if(num_in_q == 0):
        #la cola esta vacia, entonces el estado del servidor pasa a estado inactivo
        server_status = IDLE
        time_next_event[2] = 10**30
    else:
        #la cola no esta vacia por lo tanto se reduce la cantidad de clientes en espera
        num_in_q -= 1

        #calcule el retraso del cliente que está comenzando el servicio y retraso total acumulado.
        delay = time - time_arrival[1]
        total_of_delays += delay

        #incrementa el numero de clientes retrasados
        num_custs_delayed += 1
        time_next_event[2] = time + expon(mean_service)

        #mueva a cada cliente en la cola un lugar
        for i in range(num_in_q):
            time_arrival[i+1] = time_arrival[i+2]


def report():
    global total_of_delays
    global num_custs_delayed
    global area_num_in_q
    global time
    global area_server_status
    global arreglo_retraso_promedio
    global arreglo_cant_personas_cola
    global arreglo_utilizacion_servidor
    global arreglo_tiempo_total

    #calcular y escribie estimaciones del rendimiento en el registro.
    f = open("mm1.txt", "a")

    f.write("\nRetraso promedio en cola: " + str(total_of_delays / num_custs_delayed)+" min")
    f.write("\nCantidad prom. personas en cola: " + str(area_num_in_q/time))
    #f.write("\nUtilizacion del servidor: " + str(area_server_status / time)+"\%")
    f.write("\nTiempo total de la simulacion: " + str(time)+" min\n")

    arreglo_retraso_promedio.append(total_of_delays / num_custs_delayed)

    arreglo_cant_personas_cola.append(area_num_in_q/time)
    arreglo_utilizacion_servidor.append(area_server_status/time)
    arreglo_tiempo_total.append(time)

def update_time_avg_stats():
    global time
    global time_last_event
    global area_num_in_q
    global num_in_q
    global area_server_status

    #calcula el tiempo desde el ultimo evento y actualiza la marca last_event_time
    time_since_last_event = time - time_last_event
    time_last_event = time

    area_num_in_q += num_in_q * time_since_last_event
    area_server_status += server_status * time_since_last_event


def expon(mean):
    u = random.random()
    return - mean * math.log(u, math.e)


def createFile():
    if os.path.exists("mm1.txt"):
        os.remove("mm1.txt")
    open("mm1.txt", "x")


for i in range (1000):
    main()

#plt.plot(arreglo_tiempo_total)




i = 0
acumulador = 0
arreglo = []

for elemento in arreglo_retraso_promedio:
    i += 1
    acumulador += elemento
    arreglo.append(acumulador/i)

plt.plot(arreglo, label="Python")

plt.axhline(y=0.4667, color='r', linestyle='-',label="Supositorio.com")
plt.legend()
plt.title("Retraso promedio en cola", fontdict=None, loc='center', pad=None)
plt.show()
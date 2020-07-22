import math
import os
import sys
import random

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

def main():
    global mean_service
    global mean_interarrival
    global num_delays_required
    global num_custs_delayed
    global num_events

    #Se establecen los parametros
    num_events = 2
    mean_service = 0.5
    mean_interarrival = 1
    num_delays_required = 1000

    initialize()

    f = open("mm1.txt", "a")
    f.write("\nParametros ingresados:")
    f.write("\nTiempo promedio entre arribos (en minutos): " + str(mean_interarrival))
    f.write("\nTiempo promedio de servicio (en minutos): " + str(mean_service))
    f.write("\nNumero de clientes " + str(num_delays_required))

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

    #programa el siguiente arrivo
    time_next_event[1] = time + expon(mean_interarrival)

    #valida si el servidor esta ocupado, entonces incrementa el numero de clientes en cola
    if(server_status == BUSY):
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

    #Comprueba si la cola esta vacia
    if(num_in_q == 0):
        #la cola esta vacia, entonces el estado del servidor pasa a estado inactivo
        server_status = IDLE
        time_next_event[2] = sys.maxsize
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
            time_arrival[i] = time_arrival[i+1]


def report():
    global total_of_delays
    global num_custs_delayed
    global area_num_in_q
    global time
    global area_server_status

    #calcular y escribie estimaciones del rendimiento en el registro.
    f = open("mm1.txt", "a")
    f.write("\nRetraso promedio en cola (en minutos): " + str(total_of_delays / num_custs_delayed))
    f.write("\nCantidad promedio de personas en cola: " + str(area_num_in_q/time))
    f.write("\nUtilizacion del servidor: " + str(area_server_status / time))
    f.write("\nTiempo en que finalizo la simulacion (en minutos): " + str(time)+"\n")


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


main()


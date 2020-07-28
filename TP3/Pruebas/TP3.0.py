import numpy as np
from array import array
import matplotlib.pyplot as pyplot

class Colas(object):

    def __init__(self):
        self.Reloj = 0.0
        self.ListaDeEventos = array('f')
        self.Paso = 0
        self.Iniciado = False
        self.TIempoUltimoEvento = 0.0
        self.ProximoEvento = ""
        self.EstadoServidor = ""
        self.TSAcumulado = 0.0
        self.CompletaronDemora = 0

        self.med_serv = med_serv
        self.med_arrib = med_arrib

    def inicializar(self):
        self.Reloj = 0
        self.TIempoUltimoEvento = 0
        self.ProximoEvento = ""
        self.EstadoServidor = "D"
        self.TSAcumulado = 0
        self.CompletaronDemora = 0

        # calcular primer arribo
        self.ListaDeEventos.append(valorPoisson(self.med_arrib))

        # print(self.ListaDeEventos)

        # se debe forzar a que el primer evento no sea una partida, ponemos bien alto el servicio
        self.ListaDeEventos.append(99999.0)
        self.Paso = 0
        self.Iniciado = False


    def run(self):
        
        # llamo a la rutina de  inicializacion
        self.inicializar()

        # Repetir hasta que el reloj >= 50, nro clientes en cola = 0 y estadoservidor = "D"
        while True:

            #llamada a la rutina de tiempos
            self.tiempos()

            # llamada a la rutina correspondiente en funcion del tipo de evento
            if(self.ProximoEvento == "ARRIBOS"):
                self.arribos()



    def tiempos(self):
        self.TiempoUltimoEvento = self.Reloj
        if(self.ListaDeEventos[0] <= self.ListaDeEventos[1]):
            self.Reloj = self.ListaDeEventos[0]
            self.ProximoEvento = "ARRIBOS"
        else:
            self.Reloj = self.ListaDeEventos[1]
            self.ProximoEvento = "PARTIDAS"

    def arribos(self):
        # un arribo genera otro arribo 
        self.ListaDeEventos[0] = self.Reloj + valorPoisson(self.med_arrib)

        # pregunto si el servidor esta desocupado
        if self.EstadoServidor == "D":
            # cambio el estado del servidor
            self.EstadoServidor = "O"

            # programo el proximo evento de partida
            self.ListaDeEventos[1] = self.Reloj + valorExponencial(self.med_serv)

            # acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)

            # actualizo la cantidad de clientes que completaron demora
            self.CompletaronDemora += 1
        
        else:
            



def valorExponencial(media):
    return np.random.exponential(1/media)

def valorPoisson(media):
    return np.random.poisson(media)

med_serv = float(input('Ingrese el tiempo medio de servicio por minuto: '))
med_arrib = float(input('Ingrese el tiempo medio de arribos por minuto: '))

cola = Colas()
cola.run()
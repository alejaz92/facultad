import numpy as np
from array import array


class Colas(object):
    
    def __init__(self):
        self.Reloj = 0.0
        self.EstadoServidor = ""
        self.ProximoEvento = ""
        self.ListaDeEventos = array('f')
        self.Cola = array('f')
        self.TSAcumulado = 0.0
        self.DemoraAcumulada = 0.0
        self.NroDeClientesEnCola = 0
        self.AreaQDeT = 0.0
        self.TiempoUltimoEvento = 0.0
        self.CompletaronDemora = 0
        self.Paso = 0
        self.TMDeServicio = float(input('Ingrese el tiempo medio de servicio: '))
        self.TMEntreArribos = (float(input('Ingrese el tiempo medio entre arribo con respecto al tiempo de servicio (porcentaje): ')) * self.TMDeServicio)      
        self.Iniciado = False

    def inicializar(self):
        
        self.Reloj = 0
        self.EstadoServidor = "D"
        self.ProximoEvento = ""
        self.TSAcumulado = 0
        self.DemoraAcumulada = 0
        self.NroDeClientesEnCola = 0
        self.AreaQDeT = 0
        self.TiempoUltimoEvento = 0
        self.CompletaronDemora = 0

        # se debe calcular el tiempo del primer arribo

        self.ListaDeEventos.append(valorExponencial(self.TMEntreArribos))
        
        # Se debe forzar a que el primer evento no sea una partida, por lo tanto hay que asignarle un valor alto
        self.ListaDeEventos.append(99999.0)
        self.Paso = 0
        self.Iniciado = False

    # se define el algoritmo o subrutina principal

    def run(self):

        # llamo a la rutina de inicializacion

        self.inicializar()

        # Repetir hasta que el reloj >= 50, el nro de clientes en cola  = 0 y estadoservidor = "D"

        while True:
            # llamada a la rutina de tiempos

            self.tiempos()

            # llamada a la rutina correspondiente en funcion del tipo de evento que ocurre

            if (self.ProximoEvento == "ARRIBOS"):
                self.arribos()
            else:
                self.partidas()
            
            if self.Reloj >= 50 and self.NroDeClientesEnCola == 0 and self.EstadoServidor == "D":
                break
        
        self.reportes()

    def arribos(self):

        # un arribo genera otro arribo

        self.ListaDeEventos[0] = self.Reloj + valorExponencial(self.TMEntreArribos)

        # pregunto si el servidor esta desocupado

        if self.EstadoServidor == "D":
            # cambio el estado del servidor a ocupado
            self.EstadoServidor = "O"

            # programo el proximo evento partida
            self.ListaDeEventos[1] = self.Reloj + valorExponencial(self.TMDeServicio)

            # acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)

            # actualizo la cantidad de clientes que completaron la demora

            self.CompletaronDemora += 1
        
        else:
            # calculo el area bajo Q(t) desde el momento actual del reloj hacia atras (TiempoUltimoEvento)
            self.AreaQDeT += (self.NroDeClientesEnCola * (self.Reloj - self.TiempoUltimoEvento))

            # Incremento la cantidad de clientes en cola en uno
            self.NroDeClientesEnCola += 1

            # guardo el valor del reloj en la posicion Nrodeclientesencola para saber cuando llega el cliente a la cola y luego poder calcular la demora
            self.Cola.append(self.Reloj)


    def partidas(self):

        # pregunto si hay clientes en cola

        if self.NroDeClientesEnCola > 0:
            # tiempo del proximo evento de partida
            self.ListaDeEventos[1] = self.Reloj + valorExponencial(self.TMDeServicio)

            # acumulo la demora acumulada como el valor  actual del reloj( cuando se le da servicio ) menos el valor del reloj cuando el cliente ingresa a la cola
            self.DemoraAcumulada += self.Reloj - self.Cola[0]

            # actualizo el contador de clientes que completaron la demora
            self.CompletaronDemora += 1

            # acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)

            # calculo el area bajo q(t) del periodo anterior (reloj - tiempoultimoevento)
            self.AreaQDeT += (self.NroDeClientesEnCola * (self.Reloj - self.TiempoUltimoEvento))

            # decremento la cantidad de clientes en cola

            self.NroDeClientesEnCola -= 1

            # llamo a la rutina encargada de gestionar la cola, en este caso devera desplazar todos los valores una posicion hacia adelante
            self.Cola.pop(0)
        else:
            # al no haber clientes en cola, establezco el estado del servidor en desocupado
            self.EstadoServidor = "D"

            # fuerza a que no haya partidas si no hay clientes atendiendo
            self.ListaDeEventos[1] = 99999.0


    def tiempos(self):
        
        self.TiempoUltimoEvento = self.Reloj
        if (self.ListaDeEventos[0] <= self.ListaDeEventos[1]):
            self.Reloj = self.ListaDeEventos[0]
            self.ProximoEvento = "ARRIBOS"
        else:
            self.Reloj = self.ListaDeEventos[1]
            self.ProximoEvento = "PARTIDAS"

    def reportes(self):
        try:
            nroCliCoProm = self.AreaQDeT / self.Reloj
        except ZeroDivisionError:
            nroCliCoProm = 0
        
        print("Nro promedio de clientes en cola: ", nroCliCoProm)

        try:
            utilPromServ = self.TSAcumulado / self.Reloj
        except ZeroDivisionError:
            utilPromServ = 0
        
        print("Utilizacion promedio de los servidores: ", utilPromServ)

        try:
            demPromCli = self.DemoraAcumulada / self.CompletaronDemora
        except ZeroDivisionError:
            demPromCli = 0
        
        print("Demora promedio de cliente: ", demPromCli)

def valorExponencial(media):
        return np.random.exponential(1/media)

# ejecucion del modelo de simulacion

simulacion = Colas()
simulacion.run()
    
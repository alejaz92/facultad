import numpy as np
from array import array
import matplotlib.pyplot as plt

l_nroCliCoProm_arr = []
l_nroCliSisProm_arr = []
l_utilPromServ_arr = []
l_demPromCli_arr = []
l_demPromCli_sist_arr = []


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
        self.TMDeServicio = 0.0
        self.TMEntreArribos = 0.0      
        self.Iniciado = False
        self.TMDeServicio = glob_TMDeServicio
        self.TMEntreArribos = glob_TMEntreArribos

        self.nroCliCoProm_arr = []
        self.nroCliSisProm_arr = []
        self.utilPromServ_arr = []
        self.demPromCli_arr = []
        self.demPromCli_sist_arr = []

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

        self.act_reportes()
        
        self.TiempoUltimoEvento = self.Reloj
        if (self.ListaDeEventos[0] <= self.ListaDeEventos[1]):
            self.Reloj = self.ListaDeEventos[0]
            self.ProximoEvento = "ARRIBOS"
        else:
            self.Reloj = self.ListaDeEventos[1]
            self.ProximoEvento = "PARTIDAS"

    def act_reportes(self):

        # promedio de clientes en cola
        try:
            nroCliCoProm = self.AreaQDeT / self.Reloj
        except ZeroDivisionError:
            nroCliCoProm = 0
        
        # print("Nro promedio de clientes en cola: ", nroCliCoProm)
        self.nroCliCoProm_arr.append(nroCliCoProm)

        # promedio de clientes en sistema
        try:
            nroCliSisProm = (self.AreaQDeT + self.TSAcumulado) / self.Reloj
        except ZeroDivisionError:
            nroCliSisProm = 0
        
        # print("Nro promedio de clientes en cola: ", nroCliCoProm)
        self.nroCliSisProm_arr.append(nroCliSisProm)

        # utilizacion del servidor
        try:
            utilPromServ = self.TSAcumulado / self.Reloj
        except ZeroDivisionError:
            utilPromServ = 0
        
        # print("Utilizacion promedio de los servidores: ", utilPromServ)
        self.utilPromServ_arr.append(utilPromServ)

        # promedio de tiempo en cola por cliente
        try:
            demPromCli = self.DemoraAcumulada / self.CompletaronDemora
        except ZeroDivisionError:
            demPromCli = 0

        # print("Demora promedio de cliente: ", demPromCli)
        self.demPromCli_arr.append(demPromCli)
        
        # promedio de tiempo en el sistema
        try:
            demPromCli_sist = (self.DemoraAcumulada + self.TSAcumulado) / self.CompletaronDemora
        except ZeroDivisionError:
            demPromCli_sist = 0

        # print("Demora promedio de cliente: ", demPromCli)
        self.demPromCli_sist_arr.append(demPromCli_sist)
    
    def reportes(self):
        l_nroCliCoProm_arr.append(self.nroCliCoProm_arr)
        l_nroCliSisProm_arr.append(self.nroCliSisProm_arr)
        l_utilPromServ_arr.append(self.utilPromServ_arr)
        l_demPromCli_arr.append(self.demPromCli_arr)
        l_demPromCli_sist_arr.append(self.demPromCli_sist_arr)


def valorExponencial(media):
        return np.random.exponential(1/media)

def ProbNClientes(MA, MS, n):
    probN = (1 - (MA / MS)) * ((MA / MS) ** n)
    return probN

def getAxis(lista, med, multi):
    std = np.std(lista)
    mini = med - multi * std
    maxi = med + multi * std
    return mini, maxi

# ejecucion del modelo de simulacion

    
n_it = int(input("Ingrese numero de iteraciones: "))
glob_TMDeServicio = (float(input('Ingrese el tiempo medio de servicio: ')) )
glob_TMEntreArribos = (float(input('Ingrese el tiempo medio entre arribo: ')) )


for i in range(n_it):
    simulacion = Colas()
    simulacion.run()

# menu para seleccionar reporte

while True:
    print("\n")
    print("\n")
    print("Seleccione su opcion de reporte: ")
    print("\n")
    print("1 - Promedio de clientes en cola")
    print("2 - Promedio de clientes en sistema")
    print("3 - Utilizacion del servidor")
    print("4 - Demora promedio en cola")
    print("5 - Demora promedio en sistema")
    print("6 - Probabilidad de n clientes en cola")
    print("7 - Probabilidades de denegacion de servicio")
    print("0 - Salir")
    menu = int(input("Opcion seleccionada: "))

    if menu == 1:
        minis = []
        maxis = []
        longi = []
        teo_arr = []
        teo = ((glob_TMEntreArribos ** 2) / (glob_TMDeServicio * (glob_TMDeServicio - glob_TMEntreArribos)))

        for i in range(n_it):
            longi.append(len(l_nroCliCoProm_arr[i]))
            mini, maxi = getAxis(l_nroCliCoProm_arr[i], teo, 3)
            minis.append(mini)
            maxis.append(maxi)
            plt.plot(l_nroCliCoProm_arr[i])

        for i in range(max(longi)):
            teo_arr.append(teo)

        min_gral = min(minis)   
        max_gral = max(maxis)

        plt.plot(teo_arr, color= "black", label= "Valor Teorico")
        plt.legend(loc= "upper right")
        plt.axis([0, min(longi), min_gral, max_gral])
        plt.title("Promedio de clientes en cola") 
        plt.show()         
        
    elif menu == 2:
        minis = []
        maxis = []
        longi = []
        teo_arr = []
        teo = ((glob_TMEntreArribos ** 2) / (glob_TMDeServicio * (glob_TMDeServicio - glob_TMEntreArribos))) + (glob_TMEntreArribos / glob_TMDeServicio)

        for i in range(n_it):
            longi.append(len(l_nroCliCoProm_arr[i]))
            mini, maxi = getAxis(l_nroCliCoProm_arr[i], teo, 3)
            minis.append(mini)
            maxis.append(maxi)
            plt.plot(l_nroCliSisProm_arr[i])
        
        for i in range(max(longi)):
            teo_arr.append(teo)

        min_gral = min(minis)   
        max_gral = max(maxis)

        plt.plot(teo_arr, color= "black", label= "Valor Teorico")
        plt.legend(loc= "upper right")
        plt.axis([0, min(longi), min_gral, max_gral])    
        plt.title("Promedio de clientes en el sistema") 
        plt.show()

    elif menu == 3:
        minis = []
        maxis = []
        longi = []
        util_teo_arr = []
        util_teo = glob_TMEntreArribos / glob_TMDeServicio
        
        for i in range(n_it):
            longi.append(len(l_utilPromServ_arr[i]))
            mini, maxi = getAxis(l_utilPromServ_arr[i], util_teo, 2)
            minis.append(mini)
            maxis.append(maxi)
            plt.plot(l_utilPromServ_arr[i])
        for i in range(max(longi)):
            util_teo_arr.append(util_teo)

        min_gral = min(minis)   
        max_gral = max(maxis)   

        
        plt.plot(util_teo_arr, color= "black", label= "Valor Teorico")
        plt.legend(loc= "upper right")
        plt.axis([0, min(longi), min_gral, max_gral])
        plt.title("Utilizacion promedio del servidor") 
        plt.show()

    elif menu == 4:
        minis = []
        maxis = []
        longi = []
        teo_arr = []
        teo = (glob_TMEntreArribos / (glob_TMDeServicio * (glob_TMDeServicio - glob_TMEntreArribos)))

        for i in range(n_it):
            longi.append(len(l_nroCliCoProm_arr[i]))
            mini, maxi = getAxis(l_nroCliCoProm_arr[i], teo, 0.1)
            minis.append(mini)
            maxis.append(maxi)
            plt.plot(l_demPromCli_arr[i])

        for i in range(max(longi)):
            teo_arr.append(teo)

        min_gral = min(minis)   
        max_gral = max(maxis)

        plt.plot(teo_arr, color= "black", label= "Valor Teorico")
        plt.legend(loc= "upper right")
        plt.axis([0, min(longi), min_gral, max_gral])
        plt.title("Promedio de demora en cola") 
        plt.show()

    elif menu == 5:
        minis = []
        maxis = []
        longi = []
        teo_arr = []
        teo = (glob_TMEntreArribos / (glob_TMDeServicio * (glob_TMDeServicio - glob_TMEntreArribos))) + (1 / glob_TMDeServicio)


        for i in range(n_it):
            longi.append(len(l_nroCliCoProm_arr[i]))
            mini, maxi = getAxis(l_nroCliCoProm_arr[i], teo, 0.1)
            minis.append(mini)
            maxis.append(maxi)
            plt.plot(l_demPromCli_sist_arr[i])

        
        for i in range(max(longi)):
            teo_arr.append(teo)

        min_gral = min(minis)   
        max_gral = max(maxis)

        plt.plot(teo_arr, color= "black", label= "Valor Teorico")
        plt.legend(loc= "upper right")
        plt.axis([0, min(longi), min_gral, max_gral])
        plt.title("Promedio de demora en el sistema") 
        plt.show()

    elif menu == 6:
        n = int(input("Ingrese valor n para probabilidad de n en cola: "))

        probN = ProbNClientes(glob_TMEntreArribos, glob_TMDeServicio, n)

        print("La probabilidad de que hayan ", n , " o mas elementos en la cola es: ", probN)

    elif menu == 7:
        arr_den = [0, 2, 5, 10, 50]

        for i in range(len(arr_den)):
            probN = ProbNClientes(glob_TMEntreArribos, glob_TMDeServicio, arr_den[i])
            print("La probabilidad de denegacion para una cola finita de tamaño ", arr_den[i] , " es: " , probN)

    elif menu == 0:
        break

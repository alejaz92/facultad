
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Generador  del medio de los cuadrados:

def Middle_Square(seed, muestras):
    print("Medio del Cuadrado")
    numlist = []
    for i in range(muestras):
        seedlength = len(str(seed))
        # The value of n must be even in order for the method to work ... 
        # It is acceptable to pad the seeds with zeros to the left in order to create an even valued n-digit (eg: 540 → 0540).
        if (seedlength % 2 != 0):  
            seedlength += 1
            seed = str(int(seed)).zfill(seedlength)

        res = str(int(seed) * int(seed)).zfill(2 * seedlength) #fill leading zeros if seed*seed is less than (2*seed) digits long

        half = int(seedlength / 2)
        seed = res[(half):(seedlength + half)]

        numlist.append(round(int(res)/100000000, 2))

    return(numlist)

# Corrida del generador del medio de los cuadrados
# seed = 4321, muestras = 100

midsquare_test = Middle_Square(4321, 100)
print(midsquare_test)


# Generador Congruencial lineal

def gcl(seed, a, c,  m, muestras):

    print("GCL")
    numlist = []

    for i in range(muestras):
        X = (a * seed + c) % m
        numlist.append(round(X/m,2))
        seed = X
    return(numlist)

# Corrida GCL
# seed = 1.5 **32, a = 11, c = 7, m= mod = 2 ** 32, muestras = 100

gcl_test = gcl(1.5**32, 11, 7, 2**32, 100)
print(gcl_test)

# Generador de Python, a traves de Numpy

import numpy as np 

def np_method(m):
    num_list = []
    for i in range(m):
        res = np.random.randint(1, 10000)
        num_list.append(round(res/10000, 2))
    return(num_list)

# Corrida generador Numpy
# muestras = 100

np_test = np_method(100)
print(np_test)

# Muestra de los nros de la pagina random.org
# muestra = 100
aux = [962,854,730,156,780,208,847,866,771,541,148,584,814,659,781,334,986,232,745,618,143,297,931,450,521,311,647,320,196,158,532,627,283,761,253,298,436,751,482,347,764,430,722,861,351,667,804,511,868,125,326,269,236,653,669,294,694,349,968,938,982,976,754,831,316,407,  1,178,725,575,426,822,469, 23, 60,906,189, 34,818, 50,994,991,801,824,101,959,726,799,923,990,364,245,672,920,403,170,113,399,753,302]

random_m = []
for i in range(len(aux)):
    random_m.append(round(aux[i]/1000, 2))
print(random_m)





# Pruebas

# Pruebas de uniformidad

# Prueba Chi Cuadrado

def chi_test(data):
    from scipy.stats import chisquare

    n = len(data)       # n = numero de datos
    c = int(n ** (1/2)) # c = numero de clases
    gl = c-1            # gl = grados de libertad

    fe = n/c

    lim_inf = 0
    lim_sup = 0.1
    fo = []         # frecuencias observadas

    for i in range(c):
        cont_obs = 0

        for u in range(n):

            if data[u] >= lim_inf and data[u] < lim_sup:
                cont_obs += 1  

        lim_inf = lim_sup
        lim_sup += 0.1
        
        fo.append(cont_obs)


    
    print(fo)          
    chi_calc = 0


    for i in range(len(fo)):
        #print(i)
        chi_calc += ((fe - fo[i]) **2) / fe
        arr_fe.append(fe)

    print(chi_calc)
    

# Prueba Kolmogorov-Smirnov

def ks_test(data):


    n = len(data)       # n = numero de datos
    c = int(n ** (1/2)) # c = numero de clases
    gl = n            # gl = grados de libertad
    vc = (1.36/(gl ** (1/2)))    # valor critico

    fe = n/c

    lim_inf = 0
    lim_sup = 0.1
    fo = []         # frecuencias observadas
    foa = []        #frecuencias observadas acumuladas
    poa = []        # probabilidad observada acumulada

    cont_obs_ac = 0
    for i in range(c):
        cont_obs = 0

        for u in range(n):

            if data[u] >= lim_inf and data[u] < lim_sup:
                cont_obs += 1 
                cont_obs_ac += 1 

        lim_inf = lim_sup
        lim_sup += 0.1
        
        foa.append(cont_obs_ac)
        poa.append(cont_obs_ac/n)
        fo.append(cont_obs)
    
    pea = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]        # probabilidad esperada acumulada
       

    dif = []

    for i in range(c):
        dif.append(abs(poa[i] - pea[i]))


    dm = max(dif)
    print(dm)


    if dm <= vc:
        rta = "Aprobado"
    else:
        rta = "Desaprobado"
    
    return rta




# Pruebas de independencia

#Prueba de corridas
#Arriba y abajo de la media

import numpy as np
def corr_updown_test(data):
    media = 0.5
    sec = []
    n1 = 0          # valores +
    n2 = 0          # valores -
    N = len(data)   # cantidad de valores
    Z = 1.96        # debido a confianza del 96%

    for i in range(N - 1):
        if data[i] > media:
            sec.append('+')
            n1 += 1
        else:
            sec.append('-')
            n2 += 1
    b = 1       # nro de corridas

    for i in range(len(sec)- 1):
        if sec[i] != sec[i + 1]:
            b += 1


    
    medb = ((2 * n1 * n2) /(n1 + n2) ) + 1
    varb = (2 * n1 * n2 * (2 * n1 * n2 - N))/((N ** 2)* (N - 1))

    lim_inf = -Z * (varb ** (1/2)) + medb
    lim_sup = Z  * (varb ** (1/2)) + medb



    if b >= lim_inf and b <= lim_sup:
        res = "Hipotesis aceptada"
    else:
        res = "Hipotesis rechazada"
    print(lim_inf)
    print(lim_sup)
    print(b)
    
    return res


# Prueba de Series

def series_test(data):

    pair= []
    N = len(data)
    n = 2
    fe = N / (n ** 2)
    chi_tab = 16.92

    for i in range(N -1):
        pair.append([data[i], data[i+1]])
    
    tabla = []
    cont00 = 0
    cont01 = 0
    cont10 = 0
    cont11 = 0

    for i in range(len(pair)):
        if pair[i][0] < 0.5 and pair[i][1] < 0.5:
            cont00 += 1
        if pair[i][0] < 0.5 and pair[i][1] >= 0.5:
            cont01 += 1
        if pair[i][0] >= 0.5 and pair[i][1] < 0.5:
            cont10 += 1
        if pair[i][0] >= 0.5 and pair[i][1] >= 0.5:
            cont11 += 1
    tabla.append(cont00)
    tabla.append(cont01)
    tabla.append(cont10)
    tabla.append(cont11)

    chi_calc = 0
    for i in range(len(tabla)):
        aux = ((fe - tabla[i]) ** 2) / fe
        chi_calc += aux

    print(chi_calc)
    print(chi_tab)

    if chi_calc <= chi_tab:
        res = "Hipotesis aceptada"
    else:
        res = "Hipotesis rechazada"
    print(res)
        


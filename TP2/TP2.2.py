
# Generador Numpy

import numpy as np 

def np_method(m):
    num_list = []
    for i in range(m):
        res = np.random.randint(1, 10000)
        num_list.append(round(res/10000, 2))
    return(num_list)


## Distribucion Uniforme
### Importaciones y parametros

import numpy as np 
import matplotlib.pyplot as plt

m = 100000 # tamaño de la muestra
a = 0  # limite inferior
b = 10  # limite superior
bins = 100

### Transformada inversa

uni_r_array = np_method(m)

uni_x_arr = []

for i in range(m):
    x = a + (b - a) * uni_r_array[i]
    uni_x_arr.append(x)

uni_x_mean = np.mean(uni_x_arr)
uni_x_var = np.var(uni_x_arr)

plt.hist(uni_x_arr, bins = bins, edgecolor= "black")
plt.title("Distribución Uniforme - Transformada Inversa")
plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

print('Media: ',uni_x_mean)
print('Varianza: ',uni_x_var)

### Metodo Numpy

uni_np_arr = []
for i in range(m):
    uni_np_arr.append(np.random.uniform(a, b))

uni_np_mean = np.mean(uni_np_arr)
uni_np_var = np.var(uni_np_arr)

plt.hist(uni_np_arr, bins = bins, color= "green", edgecolor= "black")
plt.title("Distribución Uniforme - Método Numpy")
plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

print('Media: ',uni_np_mean)
print('Varianza: ',uni_np_var)

### Comparativa de metodos

plt.hist(uni_x_arr, bins = bins, edgecolor= "black", label= "Transformada Inversa", alpha= 0.5)       # transformada inversa
plt.hist(uni_np_arr, bins = bins, color= "green", edgecolor= "black", label= "Método Numpy", alpha = 0.5)                 #  metodo numpy
plt.plot([a, b], [m/bins, m/bins], color='black', label='Valor Teórico', linewidth=4) # teorico

plt.axis([a, b, 800, 1200])
plt.title("Distribución Uniforme - Comparativa de Métodos")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.legend(loc="lower center")
plt.show()



## Distribucion Exponencial
### Importaciones y Parametros

import numpy as np 
import matplotlib.pyplot as plt 
from math import log
import math

m = 5000     # nro de muestras
alpha = 0.15
bins = 50

### Transformada inversa

exp_r_array = np_method(m)

exp_x_arr = []
x = 0
for i in range(m):
    r = exp_r_array[i]
    x = (-1/alpha) * log(r)
    exp_x_arr.append(x)

exp_x_mean = np.mean(exp_x_arr)
exp_x_var = np.var(exp_x_arr)

plt.hist(exp_x_arr, bins= bins, edgecolor= "black")
plt.title("Distribucion Exponencial - Transformada Inversa")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
#plt.axis([0, 40, 0, 9000])
plt.show()

print('Media: ',exp_x_mean)
print('Varianza: ',exp_x_var)

### Metodo Numpy

exp_np_arr = []
for i in range(m):
    exp_np_arr.append(np.random.exponential(1/alpha))

exp_np_mean = np.mean(exp_np_arr)
exp_np_var = np.var(exp_np_arr)

plt.hist(exp_np_arr, bins = bins, color= "green", edgecolor= "black")
plt.title("Distribución Exponencial - Método Numpy")
# plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

print('Media: ',exp_np_mean)
print('Varianza: ',exp_np_var)

### Comparativa de metodos

plt.hist(exp_np_arr, bins, color= "green", edgecolor= "black", weights=np.zeros_like(exp_np_arr)+1/m, alpha = 0.5, label= "Método Numpy")
plt.hist(exp_x_arr, bins, edgecolor= "black", weights=np.zeros_like(exp_x_arr)+1/m, alpha = 0.5, label= "Transformada Inversa")
plt.plot(t, alpha * math.e**(-alpha*t), color = "black", linewidth = 4, label= "Valor Teórico")

plt.title("Distribución Exponencial - Comparativa de Métodos")
# plt.axis([0, 25 , 0, 0.2])
plt.xlabel("Rango")
plt.ylabel("Frecuencia relativa")
plt.legend(loc="upper right")
plt.show()



## Distribucion Gamma

### Importaciones y Parametros

import numpy as np 
import matplotlib.pyplot as plt 
from math import log
import math

m = 10000     # nro de muestras
alpha = 0.2
k = 5
bins = 50

### Algoritmo generador

erl_x_arr = []
for j in range(m):

    prod = 1

    for i in range(k):
        prod = prod * np.random.uniform(0, 1)

    x = -(1 / alpha) * math.log(prod, math.e)
    erl_x_arr.append(x)


print("Media: ", np.mean(erl_x_arr))
print("Varianza: ", np.var(erl_x_arr))

plt.hist(erl_x_arr, bins, label= "Algoritmo generador", edgecolor= "black")
plt.title("Distribución Erlang (Gamma) - Algoritmo generador")
# plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()



## Distribucion Normal

### Importaciones y Parametros

import numpy as np 
import matplotlib.pyplot as plt 
from math import log
import math
import scipy.stats as stats

m = 10000     # nro de muestras
mu = 10
sigma = 1
k = 12
bins = 50

### Metdo Numpy

norm_np_array = []
for i in range(m):
    x = np.random.normal(mu, sigma)
    norm_np_array.append(x)

print("Media: ", np.mean(norm_np_array))
print("Varianza: ", np.var(norm_np_array))


plt.hist(norm_np_array, bins, color= "green", edgecolor= "black", weights=(np.zeros_like(norm_np_array) + 1./len(norm_np_array))*(bins/mu))
plt.title("Distribución Normal - Método Numpy")
# plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

### Metodo del teorema central del limite

norm_x_array = []
for i in range(m):
    sum = 0
    for i in range(0, k):
        sum += np_method(1)[0]
    norm_x_array.append((sigma * ((12 / k) ** (1/2)) * (sum - (k / 2))) + mu)

print("Media: ", np.mean(norm_x_array))
print("Varianza: ", np.var(norm_x_array))

plt.hist(norm_x_array, bins, edgecolor= "black", label= "Metodo TCL", weights=(np.zeros_like(norm_x_array) + 1./len(norm_x_array))*(bins/mu))
plt.title("Distribución Normal- Método TCL")
# plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

### Comparativa 

plt.hist(norm_x_array, bins, edgecolor= "black", label= "Método TCL", weights=(np.zeros_like(norm_x_array) + 1./len(norm_x_array))*(bins/mu), alpha= 0.5)
plt.hist(norm_np_array, bins, color= "green", edgecolor= "black", weights=(np.zeros_like(norm_np_array) + 1./len(norm_np_array))*(bins/mu), label= "Método Numpy", alpha= 0.5)

# Normal teorica
x = np.linspace(mu - 5*sigma, mu + 5*sigma, m)
plt.plot(x, stats.norm.pdf(x, mu, sigma), label="Normal Teórica", color= "black", linewidth= 2)

plt.title("Distribución Normal- Comparativa")
# plt.axis([a, b, 0, 1200])
plt.legend(loc= "upper right")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()



## Distribucion Binomial

### Importaciones y parametros

import numpy as np 
import matplotlib.pyplot as plt
from math import factorial

m = 10000     # nro de muestras
n = 10
p = 0.4


### Funciones auxiliares

#### generador valores de distribucion binomial
def generar_valor(n, p):
    x = 0
    for i in range(n):
        r = np_method(1)
        if(r[0] - p <=0):
            x = x + 1
    return x

#### generador numeros combinatorios

def combinatorio(m, n):
    return(factorial(m) // (factorial(n) * factorial(m - n)))

### Algoritmo generador

bin_x_arr = []

for i in range(m):
    bin_x_arr.append(generar_valor(n, p))

esp = np.mean(bin_x_arr)
print("Media: ", esp)
var = np.var(bin_x_arr)
print("Varianza: ", var)

plt.hist(bin_x_arr, bins= np.arange(0, n, 0.5), edgecolor= "black", label= "Algoritmo Generador")
plt.title("Distribución Binomial- Algoritmo Generador")
# plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

### Metodo Numpy

bin_np_arr = np.random.binomial(n, p, m)

esp = np.mean(bin_np_arr)
print("Media: ", esp)
var = np.var(bin_np_arr)
print("Varianza: ", var)

plt.hist(bin_np_arr, bins= np.arange(0, n, 0.5), color= "green", edgecolor= "black", label= "Metodo Numpy" )
plt.title("Distribución Binomial- Método Numpy")
# plt.axis([a, b, 0, 1200])
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

### Comparativa

plt.hist(bin_np_arr, bins= np.arange(0, n, 0.5), color= "green", edgecolor= "black", label= "Metodo Numpy", alpha= 0.5, weights= np.zeros_like(bin_np_arr) + 1. / len(bin_np_arr))
plt.hist(bin_x_arr, bins= np.arange(0, n, 0.5), edgecolor= "black", label= "Algoritmo Generador", alpha= 0.5, weights= np.zeros_like(bin_x_arr) + 1. / len(bin_x_arr))


# Valor teorico

b = True

for i in range(n):
    if(b):
        plt.scatter(i + 0.25, combinatorio(n, i) * (p ** i) * ((1 - p) ** (n - i)), s= 60, zorder= 200, color= "yellow", edgecolors= "black", linewidths= 1, label= "Valor Teórico")
        b = False
    else:
        plt.scatter(i + 0.25, combinatorio(n, i) * (p ** i) * ((1 - p) ** (n - i)), s = 60, zorder= 200,  color= "yellow", edgecolors= "black", linewidths= 1,)

plt.title("Distribución Binomial- Comparativa")
# plt.axis([a, b, 0, 1200])
plt.legend(loc= "upper right")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()



## Hipergeometrica

### Importaciones y parametros

import numpy as np 
import matplotlib.pyplot as plt
from math import factorial

### Algoritmo generador

def hipergeom(tn, ns, p):
    x = 0
    for i in range(ns):
        r = np_method(1)
        if(r[0] - p <= 0):
            s = 1
            x += 1
        else:
            s = 0
        p = (tn * p - s) / (tn - 1)
        tn = tn - 1
    return x, p


m = 10000    # nro de muestras
TN =  10000         # tamaño poblacion
ns =  1000         # tamaño muestra
p = 0.8
bins = 50

hip_x_arr = []
for i in range(m):
    tn = TN
    x, p = hipergeom(tn, ns, p)
    hip_x_arr.append(x)


esp = np.mean(hip_x_arr)
print("La media es: ", esp)
var = np.var(hip_x_arr)
print("La varianza es: ", var)

plt.hist(hip_x_arr, bins, edgecolor = "black", label="Algoritmo generador", linewidth = 0.5)
plt.title("Distribucion Hipergeométrica - Algoritmo generador")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()



## Poisson

### Importaciones y parametros

import numpy as np 
import matplotlib.pyplot as plt
from math import exp

m = 10000     # nro de muestras
p = 5
bins = 100

### Algoritmo generador

poi_x_arr = []
for i in range(m):
    x = 0
    tr = 1
    b = math.exp(-p)
    flag = True
    while(flag):
        r = np_method(1)
        tr = tr * r[0]
        if(tr - b > 0):
            x += 1
        else:
            flag = False
    
    poi_x_arr.append(x)

esp = np.mean(poi_x_arr)
print("La media es: ", esp)
var = np.var(poi_x_arr)
print("La varianza es es: ", var)

plt.hist(poi_x_arr, bins, edgecolor= "black", linewidth= 0.5, label= "Algoritmo Generador")
plt.title("Distribución Poisson - Algoritmo Generador")
# plt.axis([a, b, 0, 1200])
# plt.legend(loc= "upper right")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

### Metodo Numpy

poi_np_arr = np.random.poisson(p, m)

esp = np.mean(poi_np_arr)
print("La media es: ", esp)
var = np.var(poi_np_arr)
print("La varianza es es: ", var)

plt.hist(poi_np_arr, bins, color= "green", edgecolor= "black", linewidth= 0.5, label= "Método Numpy")
plt.title("Distribución Poisson - Método Numpy")
# plt.axis([a, b, 0, 1200])
# plt.legend(loc= "upper right")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

### Comparativa

plt.hist(poi_x_arr, bins= 100, edgecolor= "black", linewidth= 0.5, label= "Algoritmo Generador", alpha= 0.5, weights= np.zeros_like(poi_x_arr) + 1. / len(poi_x_arr))
plt.hist(poi_np_arr, bins= 100, color= "green", edgecolor= "black", linewidth= 0.5, label= "Método Numpy", alpha= 0.5, weights= np.zeros_like(poi_np_arr) + 1. / len(poi_np_arr))



# Valor teorico

b = True

for i in range(16):
    if(b):
        plt.scatter(i +0.05, exp(-p) * ((p ** i) / factorial(i)), s= 60, zorder= 200, color= "yellow", edgecolors= "black", linewidths= 1, label= "Valor Teórico")
        b = False
    else:
        plt.scatter(i + 0.05, exp(-p) * ((p ** i) / factorial(i)), s = 60, zorder= 200,  color= "yellow", edgecolors= "black", linewidths= 1,)

plt.title("Distribución Poisson- Comparativa")
# plt.axis([a, b, 0, 1200])
plt.legend(loc= "upper right")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()




## Pascal (Binomial negativa)

### Importaciones y parametros

import numpy as np 
import matplotlib.pyplot as plt
from math import log 

m = 10000 # nro de muestras
k = 5 # nro de exitos necesarios
q = 0.2 # 1 - probabilidad de exitos
bins = 50


pas_x_arr = []
for i in range(m):
    tr = 1
    qr = log(q)
    for j in range(k):
        r = np_method(1)
        tr = tr * r[0]
    x = log(tr) / qr
    pas_x_arr.append(x)

esp = np.mean(pas_x_arr)
print("La media es: ", esp)
var = np.var(pas_x_arr)
print("La varianza es: ", var)
plt.hist(pas_x_arr, bins, edgecolor= "black", label= "Algoritmo Generador")

plt.title("Distribución de Pascal - Algoritmo generador")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()



## Empirica Discreta

### Importaciones y parametros

import numpy as np 
import matplotlib.pyplot as plt
import random

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
fa = [0.1, 0.2, 0.4, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1]


### Forma teorica

# CARGO UN ARREGLO CON 100 VALORES
# EN BASE A LAS FRECUENCIAS ACUMULADAS

arreglo = []
for i in range(10):
    arreglo.append(1)
    arreglo.append(2)
    arreglo.append(5)
    arreglo.append(6)

for i in range(20):
    arreglo.append(3)
    arreglo.append(4)

for i in range(5):
    arreglo.append(7)
    arreglo.append(8)
    arreglo.append(9)
    arreglo.append(10)

esp = np.mean(arreglo)
print("Media: ", esp)
var = np.var(arreglo)
print("Varianza: ", var)

plt.hist(arreglo, bins = len(arreglo), weights= np.zeros_like(arreglo) + 1. / len(arreglo), color= "green", linewidth= 7, edgecolor= "green")
plt.title("Distribución Empírica Discreta - Valores teóricos")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()

### Metodo generador

valores = []
for i in range(10000):
    r = random.uniform(0, 1)
    c = 0
    b = True

    while(b):
        if(r <= fa[c]):
            valores.append(x[c])
            b = False
        else:
            c = c + 1
esp = np.mean(valores)
print("Media: ", esp)
var = np.var(valores)
print("Varianza: ", var)


plt.hist(valores, bins= len(valores), weights= np.zeros_like(valores) + 1. / len(valores), label= "Algoritmo generador", linewidth= 7, edgecolor= "blue", color= "blue")
plt.title("Distribución Empírica Discreta - Algoritmo generador")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()


### Comparativa

plt.hist(valores, bins= len(valores), weights= np.zeros_like(valores) + 1. / len(valores), label= "Algoritmo generador", linewidth= 7, edgecolor= "blue", color= "blue", alpha = 0.5)

plt.hist(arreglo, bins = len(arreglo), weights= np.zeros_like(arreglo) + 1. / len(arreglo), color= "green", linewidth= 7, edgecolor= "green", alpha= 0.5, label= "Valor teorico")

plt.title("Distribución Empírica Discreta - Comparativa")
plt.legend(loc= "upper right")
plt.xlabel("Rango")
plt.ylabel("Frecuencia")
plt.show()


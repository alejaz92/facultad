
# %% [markdown]
# ## Importacion de paquetes

# %%
import matplotlib.pyplot as plt
import numpy as np

# %% [markdown]
# ## Promedio

# %%
tm = 5000               # Tamaño de la muestra
ex = 5                  # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta

#Experimentacion
for i in range(ex):    # Bucle para cada experimento

    arr_nro = []
    arr_prom = []
    for tir in range(1, tm + 1):    # Bucle para cada tirada
        nro_random = np.random.randint(vi, vf + 1)
        arr_nro.append(nro_random)
        prom = np.mean(arr_nro)
        arr_prom.append(prom)
    plt.plot(arr_prom)    # Grafico del experimento

# Promedio teorico
arr_pt = []
for idx in range(vi, vf + 1):
    arr_pt.append(idx)
pt = np.mean(arr_pt) # valor promedio teorico

arr_ptgraf = []
for i in range(tm):
    arr_ptgraf.append(pt)
plt.plot(arr_ptgraf, color= "black", label= "Promedio esperado")

# a continuacion detalles adicionales de graficacion
plt.axis([0, tm, pt - 5, pt + 5])
plt.title("Distribucion de los promedios")
plt.xlabel("NRO de tirada")
plt.ylabel("Promedio")
plt.legend(loc="upper right")
plt.show()

# %% [markdown]
# ## Frecuencia Relativa

# %%
tm = 5000              # Tamaño de la muestra
ex = 5                # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta
x = 5                   # Numero a evaluar



# experimentacion
for i in range(ex):    # Bucle para cada experimento
    countx = 0         # contador de cuantas veces salio x
    countt = 0         # contador de totales
    arr_frec = []      # arreglo de frecuencias

    for tir in range(1, tm + 1):    # Bucle para cada tirada
        nro_random = np.random.randint(vi, vf + 1)
        countt += 1

        if nro_random == x:
            countx += 1
        arr_frec.append(countx/countt)
    
    plt.plot(arr_frec)



# frecuencia teorica
ft = 1/(vf - vi + 1)    # Frecuencia teorica
arr_ft = []

for i in range(tm):    # Bucle para cada tirada
    arr_ft.append(ft)
plt.plot(arr_ft, color= "black", label= "Frecuencia esperada")

# a continuacion detalles adicionales de graficacion
plt.title("Frecuencia relativa de un numero X")
plt.xlabel("NRO de tirada")
plt.ylabel("Frecuencia relativa")
plt.legend(loc="upper right")
plt.axis([0, tm, ft - 0.04, ft + 0.04])
plt.show()

# %% [markdown]
# ## Varianza

# %%
tm = 5000               # Tamaño de la muestra
ex = 5                  # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta
  
# Experimentacion
for i in range(ex):    # Bucle para cada experimento

    arr_nro = []
    arr_var = []
    
    for tir in range(1, tm + 1):
        nro_random = np.random.randint(vi, vf + 1)
        arr_nro.append(nro_random)
        var = np.var(arr_nro)
        arr_var.append(var)
    plt.plot(arr_var)

# Varianza teorica
arr_vt = []
for idx in range(vi, vf + 1):
    arr_vt.append(idx)
vt = np.var(arr_vt) # valor varianza teorica

arr_vtgraf = []
for i in range(tm):
    arr_vtgraf.append(vt)
plt.plot(arr_vtgraf, color= "black", label= "Varianza esperada")

# a continuacion detalles adicionales de graficacion
plt.axis([0, tm, vt - 50, vt + 50])
plt.title("Distribucion de las Varianzas")
plt.xlabel("NRO de tirada")
plt.ylabel("Varianza")
plt.legend(loc="upper right")
plt.show()

# %% [markdown]
# ## Desvio Estandar

# %%
tm = 5000               # Tamaño de la muestra
ex = 5                  # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta

for i in range(ex):    # Bucle para cada experimento

    arr_nro = []
    arr_des = []
    
    for tir in range(1, tm + 1):
        nro_random = np.random.randint(vi, vf + 1)
        arr_nro.append(nro_random)
        des = np.std(arr_nro)
        arr_des.append(des)    
    plt.plot(arr_des)

# Desvio teorico
arr_dt = []
for idx in range(vi, vf + 1):
    arr_dt.append(idx)
dt = np.std(arr_dt) # valor desvio

arr_dtgraf = []
for i in range(tm):
    arr_dtgraf.append(dt)
plt.plot(arr_dtgraf, color= "black", label= "Desvio esperado")

# a continuacion detalles adicionales de graficacion
plt.axis([0, tm, dt -4 , dt + 4])
plt.title("Distribucion de los Desvios estandar")
plt.xlabel("NRO de tirada")
plt.ylabel("Desvio Estandar")
plt.legend(loc="upper right")
plt.show()

# %% [markdown]
# ## Histograma

# %%
tm = 5000              # Tamaño de la muestra
ex = 1                # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta
x = 5                   # Numero a evaluar

# experimentacion
for i in range(ex):    # Bucle para cada experimento

    arr_frec = []      # arreglo de frecuencias

    for tir in range(1, tm + 1):    # Bucle para cada tirada
        nro_random = np.random.randint(vi, vf + 1)
        arr_frec.append(nro_random)

    plt.hist(arr_frec, bins = vf +1)

# a continuacion detalles adicionales de graficacion
plt.title("Histograma de frecuencias")
plt.xlabel("NRO de la ruleta")
plt.ylabel("Frecuencia")
plt.show()

# %% [markdown]
# ## Mediana

# %%
tm = 5000               # Tamaño de la muestra
ex = 5                  # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta

#Experimentacion
for i in range(ex):    # Bucle para cada experimento

    arr_nro = []
    arr_med = []
    for tir in range(1, tm + 1):    # Bucle para cada tirada
        nro_random = np.random.randint(vi, vf + 1)
        arr_nro.append(nro_random)
        med = np.median(arr_nro)
        arr_med.append(med)
    plt.plot(arr_med)    # Grafico del experimento

# Mediana teorica
arr_mt = []
for idx in range(vi, vf + 1):
    arr_mt.append(idx)
mt = np.median(arr_mt) # valor de la mediana teorico

arr_mtgraf = []
for i in range(tm):
    arr_mtgraf.append(mt)
plt.plot(arr_mtgraf, color= "black", label= "Mediana esperada")

# a continuacion detalles adicionales de graficacion
plt.axis([0, tm, mt - 5, mt + 5])
plt.title("Distribucion de las Medianas")
plt.xlabel("NRO de tirada")
plt.ylabel("Mediana")
plt.legend(loc="upper right")
plt.show()

# %% [markdown]
# ## Primer Cuartil

# %%
tm = 5000               # Tamaño de la muestra
ex = 5                  # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta

#Experimentacion
for i in range(ex):    # Bucle para cada experimento

    arr_nro = []
    arr_qua = []
    for tir in range(1, tm + 1):    # Bucle para cada tirada
        nro_random = np.random.randint(vi, vf + 1)
        arr_nro.append(nro_random)
        qua = np.quantile(arr_nro, 0.25)
        arr_qua.append(qua)
    plt.plot(arr_qua)    # Grafico del experimento

# Primer cuartil teorico
arr_qt = []
for idx in range(vi, vf + 1):
    arr_qt.append(idx)
qt = np.quantile(arr_qt, 0.25) # valor del primer cuartil teorico

arr_qtgraf = []
for i in range(tm):
    arr_qtgraf.append(qt)
plt.plot(arr_qtgraf, color= "black", label= "Primer cuartil esperado")

# a continuacion detalles adicionales de graficacion
plt.axis([0, tm, qt - 5, qt + 5])
plt.title("Distribucion de los primeros cuartiles")
plt.xlabel("NRO de tirada")
plt.ylabel("Primer cuartil")
plt.legend(loc="upper right")
plt.show()

# %% [markdown]
# ## Tercer cuartil

# %%
tm = 5000               # Tamaño de la muestra
ex = 5                  # cantidad de experimentos
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta

#Experimentacion
for i in range(ex):    # Bucle para cada experimento

    arr_nro = []
    arr_qua = []
    for tir in range(1, tm + 1):    # Bucle para cada tirada
        nro_random = np.random.randint(vi, vf + 1)
        arr_nro.append(nro_random)
        qua = np.quantile(arr_nro, 0.75)
        arr_qua.append(qua)
    plt.plot(arr_qua)    # Grafico del experimento

# Tercer cuartil teorico
arr_qt = []
for idx in range(vi, vf + 1):
    arr_qt.append(idx)
qt = np.quantile(arr_qt, 0.75) # valor del tercer cuartil teorico

arr_qtgraf = []
for i in range(tm):
    arr_qtgraf.append(qt)
plt.plot(arr_qtgraf, color= "black", label= "Tercer cuartil esperado")

# a continuacion detalles adicionales de graficacion
plt.axis([0, tm, qt - 5, qt + 5])
plt.title("Distribucion de los primeros cuartiles")
plt.xlabel("NRO de tirada")
plt.ylabel("Tercer cuartil")
plt.legend(loc="upper right")
plt.show()

# %% [markdown]
# ## Diagrama de cajas

# %%
tm = 5000               # Tamaño de la muestra
vi = 0                  # valor inicial ruleta
vf = 36                 # valor final ruleta

arr_nro = []
for tir in range(1, tm + 1):    # Bucle para cada tirada
    nro_random = np.random.randint(vi, vf + 1)
    arr_nro.append(nro_random)
plt.boxplot(arr_nro)    # Grafico del experimento

# a continuacion detalles adicionales de graficacion
plt.title("Diagrama de cajas")
plt.show()


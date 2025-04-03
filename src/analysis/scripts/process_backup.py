#!/usr/bin/env python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import plfit
from pylab import *


def get_sec(array, fps):
    if not isinstance(fps, float) or fps <= 0:
        raise ValueError("La tasa de frames (fps) debe ser un valor positivo.")

    if array.ndim < 2:
        raise ValueError("El array debe tener al menos dos dimensiones.")

    array[:, 0] *= 1/fps
    return array


def check_nan(array):
    if np.isnan(array[0, 1]):
        array[0, 1] = 0.0
    return array


def tiempo_atasco(array):
    atasco = []
    atascado = True
    tiempo1 = 0.0
    for i in range(len(array)):
        if array[i][1] < 0.5:
            if not atascado:
                atascado = True
                tiempo1 = array[i][0]
        else:
            if atascado:
                atascado = False
                atasco.append(array[i][0] - tiempo1)
    return atasco


def tiempo_flujo(array):
    flujo = []
    fluyendo = False
    tiempo1 = 0.0
    for i in range(len(array)):
        if array[i][1] > 0.5:
            if not fluyendo:
                fluyendo = True
                tiempo1 = array[i][0]
        else:
            if fluyendo:
                fluyendo = False
                flujo.append(array[i][0] - tiempo1)
    return flujo



# Configuración inicial
target = sys.argv[1]
fps = float(sys.argv[3])
archivos = [file for file in os.listdir(target) if file.endswith('.csv')]
data = [np.genfromtxt(target + '/' + file, delimiter=',', dtype='float') for file in archivos]

for element in data:
    get_sec(element, fps)
    check_nan(element)

# Procesar datos
tiempos_atasco = [tiempo_atasco(element) for element in data]
tiempos_flujo = [tiempo_flujo(element) for element in data]

'''
# Validación de duraciones
suma_tiempos = [sum(tiempo_atasco) + sum(tiempo_flujo)
                for tiempo_atasco, tiempo_flujo in zip(tiempos_atasco, tiempos_flujo)]
indices_mayor_duracion = [i for i in range(len(data)) if data[i][-1, 0] > suma_tiempos[i]]
indices_menor_duracion = [i for i in range(len(data)) if data[i][-1, 0] < suma_tiempos[i]]

if indices_mayor_duracion:
    print("Duración del experimento mayor que la suma de tiempos en:")
    for index in indices_mayor_duracion:
        print(archivos[index])

if indices_menor_duracion:
    print("Duración del experimento menor que la suma de tiempos en:")
    for index in indices_menor_duracion:
        print(archivos[index])
'''


# Preparar datos para gráficos y cálculos
atascos = sorted([item for sublist in tiempos_atasco for item in sublist], reverse=True)
flujo = sorted([item for sublist in tiempos_flujo for item in sublist], reverse=True)

distribucion_de_atascos = [(i + 1) / len(atascos) for i in range(len(atascos))]
data_atasco = np.column_stack((atascos, distribucion_de_atascos))

distribucion_de_flujo = [(i + 1) / len(flujo) for i in range(len(flujo))]
data_flujo = np.column_stack((flujo, distribucion_de_flujo))

# Filtrar y calcular errores
data_atasco_filtrada = []
total_atascos = len(atascos)

duration_anterior = data_atasco[0, 0]
probability_anterior = data_atasco[0, 1]

for duration, probability in data_atasco:
    if duration < duration_anterior - 0.0005/(fps):
        binomial_error = np.sqrt(probability_anterior * (1 - probability_anterior) / total_atascos)
        data_atasco_filtrada.append((duration_anterior, probability_anterior, binomial_error))
        duration_anterior = duration
        probability_anterior = probability

binomial_error = np.sqrt(probability_anterior * (1 - probability_anterior) / total_atascos)
data_atasco_filtrada.append((data_atasco[-1, 0], data_atasco[-1, 1], binomial_error))
data_atasco_filtrada = np.array(data_atasco_filtrada)

# Guardar datos y gráficas
np.savetxt(target + '../' + sys.argv[2] + '_atasco.csv', data_atasco_filtrada,
           delimiter=',', header='Duración,Probabilidad,Binomial_Error', fmt='%.8e')

plt.figure()
plt.errorbar(data_atasco_filtrada[:, 0], data_atasco_filtrada[:, 1], 
             yerr=data_atasco_filtrada[:, 2], fmt='.', label='Error Binomial', capsize=3)
plt.xlabel('Duración del atasco (s)')
plt.ylabel('Probabilidad de atasco')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.savefig(target + '../figura_atasco.pdf')

# Graficar flujo
plt.figure()
plt.plot(data_flujo[:, 0], data_flujo[:, 1], '.', label='Probabilidad de flujo')
plt.xlabel('Duración del flujo (s)')
plt.ylabel('Probabilidad de flujo')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.savefig(target + '../figura_flujo.pdf')
np.savetxt(target + '../' + sys.argv[2] + '_flujo.csv', data_flujo, delimiter=',', fmt='%.8e')

# Ajuste de distribución de potencia
myplfit = plfit.plfit(data_atasco_filtrada[:, 0], usefortran=False)
print("----------------------------------------")
print("Pendiente Alfa: ", myplfit._alpha)
print("Error Alfa: ", myplfit._alphaerr)

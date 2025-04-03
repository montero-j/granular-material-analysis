#!/usr/bin/env python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import plfit
from pylab import *


# Tus funciones originales permanecen intactas
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


# Tu código original para cargar y preprocesar datos se mantiene
target = sys.argv[1]
fps = float(sys.argv[3])
archivos = [file for file in os.listdir(target) if file.endswith('.csv')]
data = [np.genfromtxt(target + '/' + file, delimiter=',', dtype='float') for file in archivos]

for element in data:
    get_sec(element, fps)

for element in data:
    check_nan(element)

tiempos_atasco = [tiempo_atasco(element) for element in data]
tiempos_flujo = [tiempo_flujo(element) for element in data]

# Combinación de los tiempos de atasco y flujo
atascos = [item for sublist in tiempos_atasco for item in sublist]
flujo = [item for sublist in tiempos_flujo for item in sublist]

# Ajustar la ley de potencia para los datos de atasco
atascos.sort(reverse=True)
distribucion_de_atascos = [(i + 1) / len(atascos) for i in range(len(atascos))]
data_atasco = np.column_stack((atascos, distribucion_de_atascos))

# Usar plfit para ajustar y obtener el exponente
myplfit = plfit.plfit(data_atasco[:, 0], usefortran=False)
alpha = myplfit._alpha
alpha_error = myplfit._alphaerr
x_min = myplfit._xmin

print("Exponente de la ley de potencia para atascos:", alpha)
print("Error del exponente de la ley de potencia para atascos:", alpha_error)

# Cálculo de las probabilidades acumuladas y sus errores
data_atasco_filtrada = []
duration_anterior = data_atasco[0, 0]
probability_anterior = data_atasco[0, 1]

for duration, probability in data_atasco:
    if duration < duration_anterior - 0.0005 / fps:
        data_atasco_filtrada.append((duration_anterior, probability_anterior))
        duration_anterior = duration
        probability_anterior = probability
data_atasco_filtrada.append((data_atasco[-1, 0], data_atasco[-1, 1]))

data_atasco_filtrada = np.array(data_atasco_filtrada)

# Cálculo de errores según la ley de potencia
errors_atasco = []
for duration, probability in data_atasco_filtrada:
    if duration >= x_min:
        error = probability * np.log(duration / x_min) * alpha_error
        errors_atasco.append(error)
    else:
        errors_atasco.append(0.0)

errors_atasco = np.array(errors_atasco)

# Gráfica de atasco con errores
plt.figure()
plt.errorbar(
    data_atasco_filtrada[:, 0],
    data_atasco_filtrada[:, 1],
    yerr=errors_atasco,
    fmt='o',
    label='Probabilidad de atasco (con error)'
)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Duración del atasco (s)')
plt.ylabel('Probabilidad acumulada de atasco')
plt.legend()
plt.savefig(target + '../figura_atasco_con_error.pdf')

# Guardar datos de atasco con errores
np.savetxt(
    target + '../' + sys.argv[2] + '_atasco_con_errores.csv',
    np.column_stack((data_atasco_filtrada, errors_atasco)),
    delimiter=','
)

# Repite el análisis de flujo si lo deseas con un procedimiento similar
# (puedes adaptar las líneas para "flujo" como se hizo para "atascos").

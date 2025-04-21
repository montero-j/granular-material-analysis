#!/usr/bin/env python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def cargar_measurements_en_subcarpetas(base_folder, nombre_csv='Measurements.csv'):
    """
    Busca archivos 'Measurements.csv' dentro de subcarpetas tipo sim1, sim2, ..., simN.
    Devuelve una lista de diccionarios con datos de cada archivo encontrado.
    """
    datos = []
    subcarpetas = sorted([f for f in os.listdir(base_folder) if f.startswith("sim") and os.path.isdir(os.path.join(base_folder, f))])

    for subcarpeta in subcarpetas:
        ruta_csv = os.path.join(base_folder, subcarpeta, nombre_csv)
        if os.path.exists(ruta_csv):
            try:
                data = np.genfromtxt(ruta_csv, delimiter=',', names=True)
                datos.append(data)
            except Exception as e:
                print(f"Error al leer {ruta_csv}: {e}")
        else:
            print(f"Archivo no encontrado: {ruta_csv}")
    return datos


def detectar_atascos(datos):
    """
    Detecta la duración de atascos en base a si NoPFlow == 0.
    """
    tiempos_atascos = []
    for data in datos:
        tiempo = data['Time']
        flujo_particulas = data['NoPFlow']
        atascado = flujo_particulas[0] == 0
        tiempo_inicio = tiempo[0]

        for i in range(1, len(tiempo)):
            if atascado:
                if flujo_particulas[i] > 0:
                    duracion = tiempo[i] - tiempo_inicio
                    tiempos_atascos.append(duracion)
                    atascado = False
            else:
                if flujo_particulas[i] == 0:
                    atascado = True
                    tiempo_inicio = tiempo[i]

    return tiempos_atascos


def filtrar_datos_loglog(duraciones):
    duraciones.sort(reverse=True)
    prob_acum = [(i + 1) / len(duraciones) for i in range(len(duraciones))]
    return np.column_stack((duraciones, prob_acum))


def main():
    base_folder = sys.argv[1]  # Carpeta raíz donde están sim1, sim2, ..., simN
    nombre_salida = sys.argv[2]

    datos = cargar_measurements_en_subcarpetas(base_folder)
    atascos = detectar_atascos(datos)

    if not atascos:
        print("No se detectaron atascos.")
        return

    data_loglog = filtrar_datos_loglog(atascos)

    # Gráfica sin errores
    plt.figure()
    plt.plot(data_loglog[:, 0], data_loglog[:, 1], 'o', label='Probabilidad acumulada de atasco')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Duración del atasco (s)')
    plt.ylabel('Probabilidad acumulada')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(base_folder, f'{nombre_salida}_figura_atasco.pdf'))

    # Guardar CSV
    np.savetxt(
        os.path.join(base_folder, f'{nombre_salida}_atasco.csv'),
        data_loglog,
        delimiter=',',
        header='Duracion,Probabilidad',
        comments=''
    )


if __name__ == "__main__":
    main()

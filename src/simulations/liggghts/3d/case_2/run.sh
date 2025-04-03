#!/bin/bash

# Limpiar archivos anteriores
rm -r post
rm restart*
rm log.liggghts
rm *.csv
rm *.stl
clear

# Crea las mallas
python3 generate_mesh.py
clear

# Ejecutar simulación de LIGGGHTS en segundo plano y capturar su PID
time liggghts -in input.liggghts &
LIGGHTS_PID=$!

# Manejar SIGTERM para matar solo el proceso de LIGGGHTS
trap "kill $LIGGHTS_PID; echo 'Proceso LIGGGHTS terminado'; exit 1" SIGTERM

# Esperar a que termine LIGGGHTS
wait $LIGGHTS_PID

# Verificar si la simulación generó el archivo avalanchas.csv
if [ ! -f "avalanchas.csv" ]; then
    echo "Error: No se encontró el archivo avalanchas.csv."
    exit 1
fi

# Definir la carpeta actual como ruta base
ruta_base=$(pwd)

# Crear o limpiar el archivo parametros si no existe
touch parametros
export RUTA_BASE="$ruta_base"

# Ejecutar el script de Python y redirigir la salida al archivo parametros
python3 <<EOF >> analisis
import pandas as pd
import math
import os

# Ruta base proporcionada por el script Bash
ruta_base = os.environ['RUTA_BASE']

# Ruta del archivo avalanchas.csv
archivo = os.path.join(ruta_base, 'avalanchas.csv')

# Cargar el archivo en un DataFrame
data = pd.read_csv(archivo)

# Agrupar por número de avalancha y calcular la diferencia de partículas
avalanchas = data.groupby('AvalancheCount')['NumParticlesAvalancheRealTime'].agg(['min', 'max'])
avalanchas['Particulas_salida'] = avalanchas['max'] - avalanchas['min']

# Calcular el tamaño medio de las avalanchas
tamaño_medio_avalanchas = avalanchas['Particulas_salida'].mean()

# Calcular la desviación estándar
desviacion_estandar = avalanchas['Particulas_salida'].std()

# Calcular el tamaño de la muestra
tamaño_muestra = len(avalanchas)

# Calcular el Error Estándar de la Media (SEM)
error_estandar_media = desviacion_estandar / math.sqrt(tamaño_muestra)

# Calcular las barras de error
barra_superior = tamaño_medio_avalanchas + error_estandar_media
barra_inferior = tamaño_medio_avalanchas - error_estandar_media

# Generar la salida solicitada
print(f'')
print(f'Cantidad de avalanchas: {tamaño_muestra}')
print(f'Tamaño medio de avalancha: {tamaño_medio_avalanchas:.6f}')
print(f'Desviación estándar: {desviacion_estandar:.6f}')
print(f'Error estándar de la media (SEM): {error_estandar_media:.6f}')
print(f'Barra de error superior (SEM): {barra_superior:.6f}')
print(f'Barra de error inferior (SEM): {barra_inferior:.6f}')
EOF

echo "Análisis completado y guardado en el archivo 'parametros'."


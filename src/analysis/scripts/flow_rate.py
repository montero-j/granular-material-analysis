#!/usr/bin/env python3
import sys
import pandas as pd

directory = sys.argv[1]
fps = int(sys.argv[2])

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv(directory + 'flow_rate.csv', encoding='latin-1')

# Crear una columna 'Nombre de Imagen Base' que contiene solo la parte constante del nombre de la imagen
df['Nombre de Imagen Base'] = df['Nombre de Imagen'].str.extract(r'(frame_output_medicion_\d+)_\d+.jpg')

# Agrupar por 'Nombre de Imagen Base' y sumar todas las columnas numéricas
result = df.groupby('Nombre de Imagen Base').sum(numeric_only=True).reset_index()

'''
Para hacer el calculo del flujo tener en cuenta a cuantos FPS se esta trabajando
'''

# Calcular el flujo de particulas amarillas
result['Flujo Particulas Amarillas'] = result['Particulas Amarillas'] * fps / result['Pixeles Horizontales']

# Calcular el flujo de particulas azules
result['Flujo Particulas Azules'] = result['Particulas Azules'] * fps / result['Pixeles Horizontales']

# No guardar esta columna
# result = result.drop(columns=['Nombre de Imagen'])
result = result.drop(columns=['Nombre de Imagen Base'])

# Elijo el nombre del archivo
parts = directory.split('/')
nombre_csv = parts[-3] + ".csv"

# Guardar en un archivo csv el flujo de cada tipo
result.to_csv(directory + nombre_csv, index=False)

import os
import re
import sys
import pandas as pd

# Directorio donde se encuentran los archivos CSV
directorio = sys.argv[1]
directorio_padre = os.path.dirname(directorio)
directorio_padre_2 = os.path.dirname(directorio_padre)

# Número de tirada, para el nombre del archivo
patron = r'tirada(\d+)'
match = re.search(patron, directorio)
numero_tirada = int(match.group(1))

# Crea directorios donde se guardarán posteriormente los archivos
all_folder  = os.path.join(directorio_padre_2, "data")
blue_folder  = os.path.join(all_folder, "blue")
yellow_folder = os.path.join(all_folder, "yellow")
by_folder = os.path.join(all_folder, "b+y")    
flow_folder = os.path.join(all_folder, "flow")
  
for folder in [all_folder, blue_folder, yellow_folder, by_folder, flow_folder]:
    os.makedirs(folder, exist_ok=True)

# Obtener una lista de todos los archivos en el directorio
archivos = os.listdir(directorio)

# Diccionario para agrupar los archivos por número y color
archivos_agrupados = {}

# Recorrer los archivos y agruparlos por número y color
for archivo in archivos:
    nombre_archivo, extension = os.path.splitext(archivo)
    partes_nombre = nombre_archivo.split("_")
    numero = partes_nombre[-3]
    color = partes_nombre[-1]

    if extension == ".csv" and len(partes_nombre) >= 3:
        clave = (numero, color)
        if clave not in archivos_agrupados:
            archivos_agrupados[clave] = []
        archivos_agrupados[clave].append(archivo)

# Ordenar los archivos dentro de cada grupo por número de medición
for archivos_a_combinar in archivos_agrupados.values():
    archivos_a_combinar.sort(key=lambda x: int(re.search(r'(\d+).jpg', x).group(1)))

# Función para corregir valores no válidos
def limpiar_valor(valor):
    try:
        # Intentar convertir a float directamente
        return float(valor)
    except ValueError:
        # Si falla, realizar una limpieza y retornar 0.0 en caso de error
        return float(re.sub(r'[^\d.]', '', valor) or 0)

# Combinar los archivos CSV con el mismo número y color
archivos_procesados = 0
for clave, archivos_a_combinar in archivos_agrupados.items():
    numero, color = clave
    dataframes = []
    ultima_columna_anterior = 0

    for archivo in archivos_a_combinar:
        ruta_archivo = os.path.join(directorio, archivo)
        
        # Leer el archivo CSV
        df = pd.read_csv(ruta_archivo, header=None, dtype=str)
        
        # Aplicar la función de limpieza a cada celda
        df.iloc[:, 0] = df.iloc[:, 0].apply(limpiar_valor)
        df.iloc[:, 1] = df.iloc[:, 1].apply(limpiar_valor)

        # Agregar un incremento a la primera columna del archivo actual
        df.iloc[:, 0] += ultima_columna_anterior
        ultima_columna_anterior = df.iloc[-1, 0]

        dataframes.append(df)

    # Concatenar los dataframes y guardar el archivo CSV combinado
    df_combinado = pd.concat(dataframes, axis=0, ignore_index=True)

    nombre_archivo_combinado = f"{color}_output_tirada_{numero_tirada}_medicion_{numero}.csv"
    ruta_archivo_combinado = os.path.join(directorio_padre, nombre_archivo_combinado)
    df_combinado.to_csv(ruta_archivo_combinado, index=False, header=False)
    archivos_procesados += 1

print(f"Número de archivos procesados: {archivos_procesados}")

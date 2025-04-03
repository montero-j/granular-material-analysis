import os
import subprocess
import re

def solicitar_entrada(mensaje):
    """Solicita al usuario que ingrese un valor y lo retorna."""
    return input(mensaje)

def binarizar_imagen(direccion_imagen, lower_blue, lower_green, lower_red, upper_blue, upper_green, upper_red, lower_yellow, lower_yellow_g, lower_yellow_r, upper_yellow_b, upper_yellow_g, upper_yellow_r):
    """Binariza una imagen usando el script binarize_exit.py."""
    comando = [
        "python3",
        "/home/juli/Documents/Trabajo/GranularMatter-Clogging/Análisis de Datos/binarize_exit.py",
        direccion_imagen,
        lower_blue,
        lower_green,
        lower_red,
        upper_blue,
        upper_green,
        upper_red,
        lower_yellow,
        lower_yellow_g,
        lower_yellow_r,
        upper_yellow_b,
        upper_yellow_g,
        upper_yellow_r
    ]
    subprocess.run(comando)

def combinar_csv(direccion_carpeta):
    """Combina los archivos CSV en la carpeta especificada."""
    comando = [
        "python3",
        "/home/juli/Documents/Trabajo/GranularMatter-Clogging/Análisis de Datos/combine_csv.py",
        direccion_carpeta
    ]
    subprocess.run(comando)

def mover_archivos_csv(direccion_carpeta, destino, patron):
    """Mueve los archivos CSV que coincidan con el patrón a la carpeta de destino."""
    for archivo in os.listdir(direccion_carpeta):
        if re.search(patron, archivo):
            os.rename(os.path.join(direccion_carpeta, archivo), os.path.join(destino, archivo))

def modificar_csv(direccion_carpeta, fps):
    """Modifica los archivos CSV para atascos que duraron más de 11 minutos."""
    comando = [
        "python3",
        "/home/juli/Documents/Trabajo/GranularMatter-Clogging/Análisis de Datos/modify_csv.py",
        direccion_carpeta,
        str(fps)
    ]
    subprocess.run(comando)

def procesar_duracion_atascos(direccion_carpeta, nombre_archivo, fps):
    """Procesa la duración de los atascos en la carpeta especificada."""
    comando = [
        "python3",
        "/home/juli/Documents/Trabajo/GranularMatter-Clogging/Análisis de Datos/process.py",
        direccion_carpeta,
        nombre_archivo,
        str(fps)
    ]
    subprocess.run(comando)

def calcular_flujo_descarga(direccion_carpeta, fps):
    """Calcula el flujo de descarga en la carpeta especificada."""
    comando = [
        "python3",
        "/home/juli/Documents/Trabajo/GranularMatter-Clogging/Análisis de Datos/flow_rate.py",
        direccion_carpeta,
        str(fps)
    ]
    subprocess.run(comando)

def mover_archivos_flujo(direccion_carpeta, destino):
    """Mueve los archivos CSV del flujo a la carpeta de destino."""
    for archivo in os.listdir(direccion_carpeta):
        if archivo.endswith(".csv"):
            os.rename(os.path.join(direccion_carpeta, archivo), os.path.join(destino, archivo))




if __name__ == "__main__":
    # Solicitar entradas al usuario
    direccion = solicitar_entrada("Introduzca direccion de los datos: ")
    fps = int(solicitar_entrada("Introduzca el número de frames por segundo: "))
    longitud_bucle = int(solicitar_entrada("Introduzca numero de tiradas: "))
    print("\n")

    # Solicitar valores BGR para azul y amarillo
    print("----------------------------------------")
    print("Valores BGR para Azul:")
    lower_blue_b = solicitar_entrada("Introduzca el valor de Blue Lower: ")
    lower_blue_g = solicitar_entrada("Introduzca el valor de Green Lower: ")
    lower_blue_r = solicitar_entrada("Introduzca el valor de Red Lower: ")
    upper_blue_b = solicitar_entrada("Introduzca el valor de Blue Upper: ")
    upper_blue_g = solicitar_entrada("Introduzca el valor de Green Upper: ")
    upper_blue_r = solicitar_entrada("Introduzca el valor de Red Upper: ")

    print("----------------------------------------")
    print("Valores BGR para Amarillo:")
    lower_yellow_b = solicitar_entrada("Introduzca el valor de Blue Lower: ")
    lower_yellow_g = solicitar_entrada("Introduzca el valor de Green Lower: ")
    lower_yellow_r = solicitar_entrada("Introduzca el valor de Red Lower: ")
    upper_yellow_b = solicitar_entrada("Introduzca el valor de Blue Upper: ")
    upper_yellow_g = solicitar_entrada("Introduzca el valor de Green Upper: ")
    upper_yellow_r = solicitar_entrada("Introduzca el valor de Red Upper: ")

    # Binarizar imágenes
    print("----------------------------------------")
    print("Binarizando imágenes...")
    for i in range(1, longitud_bucle + 1):
        direccion_imagen = os.path.join(direccion, f"tirada{i}")
        binarizar_imagen(direccion_imagen, lower_blue_b, lower_blue_g, lower_blue_r, upper_blue_b, upper_blue_g, upper_blue_r, lower_yellow_b, lower_yellow_g, lower_yellow_r, upper_yellow_b, upper_yellow_g, upper_yellow_r)
   
    # Combinar archivos CSV
    print("----------------------------------------")
    print("Combinando archivos CSV...")
    for i in range(1, longitud_bucle + 1):
        direccion_carpeta = os.path.join(direccion, f"tirada{i}", "csv")
        combinar_csv(direccion_carpeta)

    # Mover archivos CSV amarillos
    print("----------------------------------------")
    print("Moviendo archivos CSV amarillos...")
    for i in range(1, longitud_bucle + 1):
        patron = "^yellow.*\.csv$"
        direccion_carpeta = os.path.join(direccion, f"tirada{i}")
        destino = os.path.join(direccion, "data", "yellow")
        mover_archivos_csv(direccion_carpeta, destino, patron)

    # Mover archivos CSV azules
    print("----------------------------------------")
    print("Moviendo archivos CSV azules...")
    for i in range(1, longitud_bucle + 1):
        patron = "^blue.*\.csv$"
        direccion_carpeta = os.path.join(direccion, f"tirada{i}")
        destino = os.path.join(direccion, "data", "blue")
        mover_archivos_csv(direccion_carpeta, destino, patron)

    # Modificar archivos CSV para atascos largos
    print("----------------------------------------")
    print("Modificando archivos CSV para atascos largos...")
    direccion_yellow = os.path.join(direccion, "data", "yellow/")
    direccion_blue = os.path.join(direccion, "data", "blue/")
    modificar_csv(direccion_yellow, fps)
    modificar_csv(direccion_blue, fps)

    # Procesar duración de atascos
    print("----------------------------------------")
    print("Procesando duración de atascos...")
    nombre_archivo_blue = "data_blue"
    nombre_archivo_yellow = "data_yellow"
    #procesar_duracion_atascos(direccion_blue, nombre_archivo_blue, fps)
    procesar_duracion_atascos(direccion_yellow, nombre_archivo_yellow, fps)

    # Calcular flujo de descarga
    #print("Calculando flujo de descarga...")
    #for i in range(1, longitud_bucle + 1):
    #    direccion_carpeta = os.path.join(direccion, f"tirada{i}/flow/")
    #    calcular_flujo_descarga(direccion_carpeta, fps)

    # pasar esto a python

    # # Mover el archivo CSV del flujo
    # for ((i=1; i<=longitud_bucle; i++)); do
    # 	for F in ${direccion}/tirada$i/flow/*.csv; do
    # 		mv "$F" ${direccion}/data/flow/
    # 	done
    # done

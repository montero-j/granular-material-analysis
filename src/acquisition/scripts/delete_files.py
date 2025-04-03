#!/usr/bin/env python3

import os
import shutil

def eliminar(ruta):
    if os.path.exists(ruta):
        try:
            if os.path.isfile(ruta):
                os.remove(ruta)
                #print(f"El archivo {ruta} ha sido eliminado.")
            elif os.path.isdir(ruta):
                shutil.rmtree(ruta)
                #print(f"El directorio {ruta} y su contenido han sido eliminados.")
        except OSError as e:
            print(f"No se pudo eliminar el archivo o directorio {ruta}: {e}")
    else:
        print(f"No se encontró el archivo o directorio {ruta}.")

def crear_directorio(ruta):
    try:
        os.makedirs(ruta)
        #print(f"Directorio {ruta} creado exitosamente.")
    except OSError as e:
        print(f"No se pudo crear el directorio {ruta}: {e}")

def main():
    ruta_elemento = "ruta/al/archivo_o_directorio"  # Reemplaza con la ruta de tu archivo o directorio
    try:
        eliminar(ruta_elemento)
    except Exception as e:
        print(f"Se produjo un error al eliminar el archivo o directorio: {e}")

if __name__ == "__main__":
    main()

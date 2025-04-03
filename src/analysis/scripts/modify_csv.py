import os
import csv
import sys



def fps_frame(fps):
    '''
    Esta funcion calcula la cantidad de frames que equivalen a 10 min de filmacion, 
    esto depende de los FPS empleados durante la filmacion.
    
    Args:
        FPS con los que se realizo la filmacion.

    Return:
        Frames equivalentes a una filmacion de 10 minutos.

    '''
    if fps == 480:
        frame = 261680#288000-480
    
    if fps == 220:#600:
        frame = 131000#360000#
    
    if fps == 800:
        frame = 480000
    
    return frame    



def update_csv(filename, frame):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Buscar el último 1.0 en la segunda columna
    last_one_index = -1
    for i in range(len(rows) - 1, -1, -1):
        if rows[i][1] == '1.0':
            last_one_index = i
            break

    # Verificar si hay una separación de X elementos desde el último 1.0
    # Este valor depende de a que FPS estoy filmando, 
    
    if len(rows) - 1 - last_one_index >= frame:
        # Cambiar el último elemento de la segunda columna a 1.0
        rows[-1][1] = '1.0'

    # Escribir los cambios en el archivo
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


if __name__ == "__main__":
    
    
    framerate = sys.argv[2]
    folder_path = sys.argv[1]  # Ruta de la carpeta que contiene los archivos CSV
    frames = fps_frame(int(framerate))
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            update_csv(file_path, frames)

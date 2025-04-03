#!/usr/bin/env python3

import sys
import cv2
import glob
import numpy as np

def combine(counter, path=None):
    
    """
    Combina los frames individuales de un video en un archivo de imagen de salida.

    Requiere un argumento:
        1. Ruta base de los archivos de imagen (directorio que contiene los frames).

    La función busca los archivos de imagen en el directorio según un patrón específico y los combina en lotes.
    Cada lote se guarda como un archivo de imagen de salida. El tamaño del lote se especifica mediante `batch_size`.

    El archivo de salida tiene un formato de nombre específico, con un contador que se incrementa para cada lote generado.

    Returns:
        0: Si el proceso se completó correctamente.

    Ejemplo de uso:
        python3 script.py path/to/frames/
    """

    if path is None:
        if len(sys.argv) < 2:
            print("Se requiere un argumento: Ruta base de los archivos de imagen.")
            return 1

        path = sys.argv[1]  # Ruta base de los archivos de imagen

    pattern = f"{path}/frames/frame_*.jpg"  # Patrón para buscar archivos de imagen

    try:
        PathList = glob.glob(pattern)
        PathList.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

        output_counter = 1  # Contador para el nombre del archivo de salida
        batch_size = 32500  # Tamaño del lote

        # Leer la primera imagen para obtener las dimensiones
        first_img = cv2.imread(PathList[0])
        img_height, img_width, img_channels = first_img.shape

        # Crear el array para almacenar las imágenes del lote
        batch_images = np.empty((batch_size, img_width, 1, img_channels), dtype=np.uint8)
        batch_index = 0  # Índice para rastrear la posición actual en el lote

        for file_path in PathList:
            img = cv2.imread(file_path)
            img = cv2.rotate(img[7:8, :], cv2.ROTATE_90_COUNTERCLOCKWISE)

            batch_images[batch_index] = img
            batch_index += 1

            # Guardar el lote actual y reiniciar si se alcanza el tamaño del lote
            if batch_index == batch_size:
                full_image = np.hstack(batch_images)
                output_path = f"{path}/frame_output_medicion_{counter}_{output_counter}.jpg"
                cv2.imwrite(output_path, full_image)
                output_counter += 1

                # Reiniciar el lote
                batch_images = np.empty((batch_size, img_width, 1, img_channels), dtype=np.uint8)
                batch_index = 0

        # Guardar el último lote si no se alcanza el tamaño del lote completo
        if batch_index > 0:
            batch_images = batch_images[:batch_index]
            full_image = np.hstack(batch_images)
            output_path = f"{path}/frame_output_medicion_{counter}_{output_counter}.jpg"
            cv2.imwrite(output_path, full_image)

        cv2.destroyAllWindows()

        return 0

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(combine())

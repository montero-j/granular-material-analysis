#!/usr/bin/env python3

import cv2
import sys
import os


def cut_video(video_path=None, output_dir=None):
    """
    Separa un archivo de video en frames individuales y los guarda en un directorio.

    Requiere dos argumentos:
        1. Dirección del video.
        2. Directorio de salida (string).

    Si el directorio de salida ya contiene archivos de imagen, el proceso se omitirá.

    Returns:
        0: Si el proceso se completó correctamente.
        1: Si se produjo un error.

    Ejemplo de uso:
        python3 script.py video.mp4 "/home/juli/Documentos/Mediciones/frames"
    """

    if video_path is None or output_dir is None:
        if len(sys.argv) < 3:
            print("Se requieren dos argumentos: dirección del video y directorio de salida.")
            return 1

        video_path = sys.argv[1]
        output_dir = sys.argv[2]

    # Verificar si el directorio de salida existe
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Error al crear el directorio de salida: {e}")
            return 1

    # Verificar si el directorio de salida contiene archivos de imagen
    if len(os.listdir(output_dir)) == 0:
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                print("No se pudo abrir el archivo de video.")
                return 1

            i = 0
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                output_path = os.path.join(output_dir, f'frame_{i}.jpg')
                cv2.imwrite(output_path, frame)
                i += 1

            cap.release()
            cv2.destroyAllWindows()

        except cv2.error as e:
            print(f"Error al procesar el video: {e}")
            return 1

    else:
        print("El directorio de salida ya contiene archivos de imagen. No se realizará el proceso.")

    return 0


if __name__ == "__main__":
    sys.exit(cut_video())


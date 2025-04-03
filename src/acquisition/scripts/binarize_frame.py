import sys
import cv2
import numpy as np

def color_particle(ultima_imagen):
    """
    Esta función realiza un análisis de imagen para detectar un determinado color RGB.

    Args:
        ultima_imagen: Imagen a analizar.

    Returns:
        True si se detecta amarillo en al menos el 10% de la imagen, False en caso contrario.
    """
    try:
        # Constantes
        
        LOWER_YELLOW = np.array([41, 94, 98])
        UPPER_YELLOW = np.array([105, 153, 161])
        
        KERNEL = np.ones((3, 3), np.uint8)

        # Aplicar filtro de color
        mask = cv2.inRange(ultima_imagen, LOWER_YELLOW, UPPER_YELLOW)

        # Eliminar ruido
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=3)

        # Contar píxeles blancos en la máscara
        total_pixels = mask.shape[0] * mask.shape[1]
        white_pixels = np.count_nonzero(mask)

        # Verificar si al menos el 5% de los píxeles son blancos
        if white_pixels >= 0.05 * total_pixels:
            return True
        else:
            return False

    except Exception as e:
        print("Error en color_particle:", str(e))
        return False


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            image = cv2.imread(sys.argv[1])
            result = color_particle(image)
            print(result)
        else:
            print("Debe proporcionar una imagen como argumento.")
    except Exception as e:
        print("Error en el programa principal:", str(e))

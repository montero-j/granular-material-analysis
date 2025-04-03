import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

def area_a_diametro(area):
    """
    Calcula el diámetro de una partícula esférica a partir de su área
    
    Parámetros:
      area: Área de la partícula en milímetros cuadrados.
      
    Retorno:
      Diámetro de la partícula en milímetros.
    """
    diametro = math.sqrt((4 * area) / math.pi)
    return diametro

def calcular_esfericidad(contorno):
    """
    Calcula la relación de esfericidad de un contorno.
    
    Parámetros:
        contorno: Contorno de la partícula.
        
    Retorno:
        Relación de esfericidad.
    """
    area = cv2.contourArea(contorno)
    perimetro = cv2.arcLength(contorno, True)
    radio_equivalente = perimetro / (2 * math.pi)
    area_circulo = math.pi * (radio_equivalente ** 2)
    
    if area_circulo > 0:
        esfericidad = area / area_circulo
    else:
        esfericidad = 0
    
    return esfericidad

# Cargar la imagen
imagen = cv2.imread("/media/juli/704F1AE73DAEF1F3/Documentos/GFSG/experimentos/flujo/size distribution/Ceramico/ceramico1-sin-escala.jpg")

# Descartar los primeros 750 píxeles
#imagen_recortada = imagen[:, 1447:]
imagen_recortada = imagen

# Convertir a escala de grises
gris = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2GRAY)

# Binarizar la imagen
umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Eliminar ruido
kernel = np.ones((5, 5), np.uint8)
kernel2 = np.ones((2, 2), np.uint8)

#umbral = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel, iterations = 1)
#umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel, iterations = 2)

#umbral = cv2.dilate(umbral, kernel, iterations = 1)
#umbral = cv2.erode(umbral, kernel, iterations = 1)

# Detección de contornos
contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Obtener dimensiones de la imagen
alto, ancho = umbral.shape[:2]

# Relación de conversión de píxeles a mm
pixeles_por_mm = 24  # 44 píxeles representan 1 mm

# Filtrar contornos que no están pegados al borde
contornos_filtrados = []
for contorno in contornos:
    x, y, w, h = cv2.boundingRect(contorno)
    if x > 0 and y > 0 and x + w < ancho and y + h < alto:
        area = cv2.contourArea(contorno)
        if area >= 200 and area <= 1500:  # Antes en vez de 400 estaba en 900
            contornos_filtrados.append(contorno)


# Filtrar contornos por esfericidad
umbral_esfericidad = 0.8  # Ajusta este valor según tus criterios
contornos_filtrados_esfericidad = []

for contorno in contornos_filtrados:
    esfericidad = calcular_esfericidad(contorno)
    if esfericidad >= umbral_esfericidad:
        contornos_filtrados_esfericidad.append(contorno)

# Calcular áreas de contornos filtrados y convertir a milímetros cuadrados
areas_mm2 = [cv2.contourArea(contorno) / pixeles_por_mm ** 2 for contorno in contornos_filtrados_esfericidad]

# Calcular la media de las áreas de los contornos en milímetros cuadrados
media_area_mm2 = np.mean(areas_mm2)

# Calcular el error estándar de la media
error_estandar_media_mm2 = np.std(areas_mm2) / np.sqrt(len(areas_mm2))

# Calcular diámetros de contornos filtrados
diametros_mm = [area_a_diametro(area) for area in areas_mm2]

# Calcular la media del diámetro de los contornos en milímetros
media_diametro_mm = np.mean(diametros_mm)

# Calcular el error estándar de la media
error_estandar_media_mm = np.std(diametros_mm) / np.sqrt(len(diametros_mm))

# Dibujar contornos en la imagen binarizada con diferentes colores según el tamaño y esfericidad
copia_umbral_coloreada_esfericidad = cv2.cvtColor(umbral, cv2.COLOR_GRAY2BGR)

for contorno, diametro_mm in zip(contornos_filtrados_esfericidad, diametros_mm):
    color = (0, 255, 0)  # Color por defecto para contornos normales
    if diametro_mm >= 1.2:  # Si el diámetro es mayor o igual a 1.5 cm
        color = (255, 0, 0)  # Cambiar el color a rojo
        
    cv2.drawContours(copia_umbral_coloreada_esfericidad, [contorno], -1, color, 2)


# Imprimir la cantidad de contornos después del filtro de esfericidad
print("Cantidad de contornos después del filtro de esfericidad:", len(contornos_filtrados_esfericidad))

# Imprimir la información del diámetro
print("Media del diámetro de los contornos (mm):", media_diametro_mm)
print("Error estándar de la media (mm):", error_estandar_media_mm)

# Calcular el histograma normalizado
histograma, bordes = np.histogram(diametros_mm, bins=20)
histograma_normalizado = histograma / len(contornos_filtrados_esfericidad)

# Mostrar la imagen binarizada con los contornos coloreados según el tamaño y esfericidad
plt.figure(figsize=(12, 6))

# Subplot 1: Imagen binarizada con contornos
plt.subplot(1, 2, 1)
plt.imshow(copia_umbral_coloreada_esfericidad) 
plt.title('Imagen binarizada con contornos coloreados')
plt.axis('off')

# Subplot 2: Histograma de los diámetros
plt.subplot(1, 2, 2)
plt.bar(bordes[:-1], histograma_normalizado, width=np.diff(bordes), edgecolor='black')
plt.xlabel('Diámetro (mm)')
plt.ylabel('Frecuencia normalizada')
plt.title('Histograma de diámetros')
plt.grid(True)

plt.show()

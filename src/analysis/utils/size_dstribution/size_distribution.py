import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen
imagen = cv2.imread("/home/juli/Escritorio/IM2.jpg")

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Binarizar la imagen
umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Eliminar ruido
kernel = np.ones((5, 5), np.uint8)
umbral = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel)

# Detección de contornos
contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Obtener dimensiones de la imagen
alto, ancho = umbral.shape[:2]

# Filtrar contornos que no están pegados al borde
contornos_filtrados = []
for contorno in contornos:
    x, y, w, h = cv2.boundingRect(contorno)
    if x > 0 and y > 0 and x + w < ancho and y + h < alto:
        contornos_filtrados.append(contorno)

# Calcular áreas de contornos filtrados
areas = [cv2.contourArea(contorno) for contorno in contornos_filtrados]

# Calcular la dispersión de tamaño
dispersion = np.std(areas)

# Dibujar contornos en la imagen binarizada
copia_umbral = cv2.cvtColor(umbral, cv2.COLOR_GRAY2BGR)
cv2.drawContours(copia_umbral, contornos_filtrados, -1, (0, 255, 0), 2)

# Mostrar la imagen binarizada con los contornos y el histograma
plt.figure(figsize=(12, 6))

# Subplot 1: Imagen binarizada con contornos
plt.subplot(1, 2, 1)
plt.imshow(copia_umbral)
plt.title('Imagen binarizada con contornos')
plt.axis('off')

# Subplot 2: Histograma de áreas de contornos
plt.subplot(1, 2, 2)
plt.hist(areas, bins=20, color='blue', edgecolor='black', alpha=0.7)
plt.xlabel('Área en pixeles')
plt.ylabel('Frecuencia')
plt.title('Histograma de áreas en pixeles')

plt.tight_layout()
plt.show()

# Imprimir la cantidad de contornos y la dispersión de tamaño
print("Cantidad de contornos:", len(contornos_filtrados))
print("Dispersión de tamaño:", dispersion)

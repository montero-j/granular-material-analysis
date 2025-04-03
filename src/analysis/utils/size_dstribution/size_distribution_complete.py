import cv2
import math
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


def procesar_imagen(imagen_path, pixeles_por_mm, area_minima):
    # Cargar la imagen
    imagen = cv2.imread(imagen_path)

    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Binarizar la imagen
    umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Eliminar ruido
    #kernel = np.ones((5, 5), np.uint8)
    #umbral = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel)

    # Detección de contornos
    contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Obtener dimensiones de la imagen
    alto, ancho = umbral.shape[:2]

    # Filtrar contornos que no están pegados al borde y cuya área sea mayor o igual a 5 píxeles
    contornos_filtrados = []
    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        if x > 0 and y > 0 and x + w < ancho and y + h < alto:
            area = cv2.contourArea(contorno)
            if area >= area_minima and area <= 10000:  # Descartar contornos con área menor a 5 píxeles 3000
                contornos_filtrados.append(contorno)


    # Filtrar contornos por esfericidad
    umbral_esfericidad = 0.8#0.8 - 06  # Ajusta este valor según tus criterios
    contornos_filtrados_esfericidad = []

    for contorno in contornos_filtrados:
        esfericidad = calcular_esfericidad(contorno)
        if esfericidad >= umbral_esfericidad:
            contornos_filtrados_esfericidad.append(contorno)


    # Calcular áreas de contornos filtrados y convertir a milímetros cuadrados
    areas_mm2 = [cv2.contourArea(contorno) / pixeles_por_mm ** 2 for contorno in contornos_filtrados_esfericidad]
    num_particulas = len(areas_mm2)
    media_area = np.mean(areas_mm2)
    dispersion = np.std(areas_mm2)
    error_estandar = np.std(areas_mm2) / np.sqrt(len(areas_mm2))

    # Calcular diámetros de contornos filtrados
    diametros_mm = [area_a_diametro(area) for area in areas_mm2]
    # Calcular la media del diámetro de los contornos en milímetros
    media_diametro_mm = np.mean(diametros_mm)
    # Calcular la dispersion
    dispersion_diametro = np.std(diametros_mm)
    # Calcular el error estándar de la media
    error_estandar_media_mm = np.std(diametros_mm) / np.sqrt(len(diametros_mm))


    return diametros_mm, num_particulas, media_diametro_mm, dispersion_diametro, error_estandar_media_mm

# Rutas de las imágenes y escalas correspondientes
imagenes_y_escalas_ceramico_area_minima = [
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Ceramico/ceramico1-sin-escala.jpg", 50, 800),
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Ceramico/ceramico2-sin-escala.jpg", 64, 800),
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Ceramico/ceramico3-sin-escala.jpg", 46, 800)
]

imagenes_y_escalas_amaranto_area_minima = [
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Amaranto/amaranto1-sin-escala.jpg", 49, 800),
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Amaranto/amaranto2-sin-escala.jpg", 45, 800),
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Amaranto/amaranto3-sin-escala.jpg", 40, 800),
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Amaranto/amaranto4-sin-escala.jpg", 44, 800)
]

imagenes_y_escalas_vidrio_area_minima = [
    ("/home/juli/Documentos/Flow/Distribucion de tamaños/Vidrio/tamizadas/vidrio1.jpg", 35, 200),
    ('/home/juli/Documentos/Flow/Distribucion de tamaños/Vidrio/tamizadas/vidrio2.jpg', 40, 200),
    ('/home/juli/Documentos/Flow/Distribucion de tamaños/Vidrio/tamizadas/vidrio3.jpg', 36, 200),
    ('/home/juli/Documentos/Flow/Distribucion de tamaños/Vidrio/tamizadas/vidrio4.jpg', 40, 200),
    ('/home/juli/Documentos/Flow/Distribucion de tamaños/Vidrio/tamizadas/vidrio5.jpg', 24, 200)
]

# Almacenar áreas de contornos y diámetros totales para cada material
diametros_totales_ceramico = []
diametros_totales_amaranto = []
diametros_totales_vidrio = []
total_particulas_ceramico = 0
total_particulas_amaranto = 0
total_particulas_vidrio = 0

for imagen_path, escala, area_minima in imagenes_y_escalas_ceramico_area_minima:
    diametros_imagen, num_particulas, _, _, _ = procesar_imagen(imagen_path, escala, area_minima)
    diametros_totales_ceramico.extend(diametros_imagen)
    total_particulas_ceramico += num_particulas

for imagen_path, escala, area_minima in imagenes_y_escalas_amaranto_area_minima:
    diametros_imagen, num_particulas, _, _, _ = procesar_imagen(imagen_path, escala, area_minima)
    diametros_totales_amaranto.extend(diametros_imagen)
    total_particulas_amaranto += num_particulas

for imagen_path, escala, area_minima in imagenes_y_escalas_vidrio_area_minima:
    diametros_imagen, num_particulas, _, _, _ = procesar_imagen(imagen_path, escala, area_minima)
    diametros_totales_vidrio.extend(diametros_imagen)
    total_particulas_vidrio += num_particulas

import matplotlib.colors as mcolors

# Obtener una lista de colores oscuros basados en la escala de colores de matplotlib
colores = ['blue', 'blue', 'blue']  # Colores base

# Guardar histogramas individuales normalizados en archivos PDF y mostrar estadísticas para cada material
materiales = ["Ceramic", "Amaranth", "Glass"]
for material, diametros_totales, total_particulas, color in zip(materiales, [diametros_totales_ceramico, diametros_totales_amaranto, diametros_totales_vidrio], [total_particulas_ceramico, total_particulas_amaranto, total_particulas_vidrio], colores):
    # Calcular histograma y bordes para el material actual
    histograma_material, bordes_material = np.histogram(diametros_totales, bins=15)
    histograma_normalizado_material = histograma_material / len(diametros_totales)
    
    # Guardar histograma individual normalizado en un archivo PDF
    plt.figure(figsize=(20,16))
    plt.bar(bordes_material[:-1], histograma_normalizado_material, width=np.diff(bordes_material), color=color, edgecolor='black', alpha=0.7, label=material)
    plt.xlabel('$d_f$[mm]', fontsize=68)
    plt.ylabel('Frequency', fontsize=68)
    # Aumentar el tamaño de los tics en los ejes x e y
    plt.xticks(fontsize=62)
    plt.yticks(fontsize=62)
    plt.yticks(np.linspace(0.0, 0.3, 4)) 
    plt.ylim(0, 0.37)
    plt.xlim(0.2, 2.5)
    
    plt.legend(handlelength=0.0, fontsize=68)
    plt.savefig(material + "_histograma_normalizado.pdf")
    plt.close()

    
    
    # Mostrar estadísticas para el material actual
    media_diametros_material = np.mean(diametros_totales)
    dispersion_material = np.std(diametros_totales)
    error_estandar_material = np.std(diametros_totales) / np.sqrt(len(diametros_totales))

    print(f"\nPara el material {material}:")
    print("Número total de partículas detectadas:", total_particulas)
    print("Diámetro medio de las partículas:", media_diametros_material)
    print("Error estándar de la media:", error_estandar_material)




# Calcular histogramas normalizados combinados para cada material
histograma_ceramico, bordes_ceramico = np.histogram(diametros_totales_ceramico, bins=20)
histograma_normalizado_ceramico = histograma_ceramico / len(diametros_totales_ceramico)

histograma_amaranto, bordes_amaranto = np.histogram(diametros_totales_amaranto, bins=20)
histograma_normalizado_amaranto = histograma_amaranto / len(diametros_totales_amaranto)

histograma_vidrio, bordes_vidrio = np.histogram(diametros_totales_vidrio, bins=20)
histograma_normalizado_vidrio = histograma_vidrio / len(diametros_totales_vidrio)

# Calcular histogramas acumulados normalizados para cada material
histograma_acumulado_normalizado_ceramico = np.cumsum(histograma_normalizado_ceramico)
histograma_acumulado_normalizado_amaranto = np.cumsum(histograma_normalizado_amaranto)
histograma_acumulado_normalizado_vidrio = np.cumsum(histograma_normalizado_vidrio)

# Mostrar histogramas acumulados
plt.figure(figsize=(8, 6))
plt.plot(bordes_ceramico[:-1], histograma_acumulado_normalizado_ceramico, color='blue', label='Ceramic')
plt.plot(bordes_amaranto[:-1], histograma_acumulado_normalizado_amaranto, color='red', label='Amaranth')
plt.plot(bordes_vidrio[:-1], histograma_acumulado_normalizado_vidrio, color='green', label='Glass')
plt.xlabel('$d_f$[mm]', fontsize=14)
plt.ylabel('Cumulative Frequency', fontsize=14)
plt.ylim(0, 1.1)  # Asegurarse de que la escala en el eje y vaya de 0 a 1 para una frecuencia acumulada
plt.xlim(0.2, 2.5)
plt.legend()  # Mostrar leyenda
plt.savefig("Histograma_Acumulado.pdf")
plt.close()

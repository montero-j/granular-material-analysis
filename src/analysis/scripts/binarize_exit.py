#!/usr/bin/env python3

import csv
import os
import sys
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
    Este código analiza las imágenes de la cámara.
    Requiere como argumentos:
        1 - Directorio de la imagen
'''

ancho_pixel_azul = 1
alto_pixel_azul = 15

ancho_pixel_amarillo = 1
alto_pixel_amarillo = 15

min_contornos = 50  # Número mínimo de contornos para generar el archivo CSV  150/2=75

def get_image_filename(directory):
    lista_imagenes = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            lista_imagenes.append(filename)
    return lista_imagenes

def paint_detected_pixels(original_image, mask, color, min_area_width=2, min_area_high=15):
    output_image = original_image.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > min_area_width and h > min_area_high:
            output_image[y:y+h, x:x+w] = color
    return output_image

def generate_signal_from_mask(mask, min_area_width=2, min_area_height=15):
    signal = np.zeros((mask.shape[1], 2))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    signal[:, 0] = np.arange(mask.shape[1])
    valid_contours = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > min_area_width and h > min_area_height:
            signal[x:x+w, 1] = 1
            valid_contours += 1
    return signal, valid_contours

def binarize_exit(Fullimage, lower_blue_b, lower_blue_g, lower_blue_r, upper_blue_b, upper_blue_g, upper_blue_r, lower_yellow_b, lower_yellow_g, lower_yellow_r, upper_yellow_b, upper_yellow_g, upper_yellow_r):
    blur = cv2.blur(Fullimage, (2,2))
    LOWER_BLUE = np.array([int(lower_blue_b), int(lower_blue_g), int(lower_blue_r)])
    UPPER_BLUE = np.array([int(upper_blue_b), int(upper_blue_g), int(upper_blue_r)])
    LOWER_YELLOW = np.array([int(lower_yellow_b), int(lower_yellow_g), int(lower_yellow_r)])
    UPPER_YELLOW = np.array([int(upper_yellow_b), int(upper_yellow_g), int(upper_yellow_r)])

    KERNEL4 = np.ones((3, 1), np.uint8)

    mask_yellow = cv2.inRange(blur, LOWER_YELLOW, UPPER_YELLOW)
    
    blur_yellow = cv2.erode(mask_yellow, KERNEL4, iterations=2)

    mask_blue = cv2.inRange(blur, LOWER_BLUE, UPPER_BLUE)
    blur_blue = mask_blue

    cv2.imwrite(mask_output_total_path.replace('.jpg', '_yellow.png'), blur_yellow)
    cv2.imwrite(mask_output_total_path.replace('.jpg', '_blue.png'), blur_blue)

    data_yellow, num_yellow_contours = generate_signal_from_mask(blur_yellow, ancho_pixel_amarillo, alto_pixel_amarillo)
    data_blue, num_blue_contours = generate_signal_from_mask(blur_blue, ancho_pixel_azul, alto_pixel_azul)

    if num_yellow_contours >= min_contornos or num_yellow_contours <= 5:
        pd.DataFrame(data_yellow).to_csv(output_csv_path.replace('.csv', '_yellow.csv'), header=None, index=None)
        plt.figure()
        plt.title(image + "-" + "yellow")
        plt.plot(data_yellow[:, 0], data_yellow[:, 1])
        plt.savefig(output_pdf_path.replace('.pdf', '_yellow.png'))
        plt.close()

    if num_blue_contours >= min_contornos or num_blue_contours <= 5:
        pd.DataFrame(data_blue).to_csv(output_csv_path.replace('.csv', '_blue.csv'), header=None, index=None)
        plt.figure()
        plt.plot(data_blue[:, 0], data_blue[:, 1])
        plt.title(image + "-" + "blue")
        plt.savefig(output_pdf_path.replace('.pdf', '_blue.png'))
        plt.close()

    return num_yellow_contours, num_blue_contours

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError("Se requiere al menos 1 argumento: directorio de la imagen.")

        directory = sys.argv[1]
        image_filename = get_image_filename(directory)

        if not image_filename:
            raise ValueError("No se encontró ninguna imagen en el directorio.")

        pdf_folder = os.path.join(directory, "pdf")
        csv_folder = os.path.join(directory, "csv")
        flow_folder = os.path.join(directory, "flow")
        mask_folder = os.path.join(directory, "mask")
        original_detected_folder = os.path.join(directory, "original_detected")

        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)
        if not os.path.exists(mask_folder):
            os.makedirs(mask_folder)
        if not os.path.exists(flow_folder):
            os.makedirs(flow_folder)
        if not os.path.exists(original_detected_folder):
            os.makedirs(original_detected_folder)

        flow_rate_csv_path = os.path.join(flow_folder, 'flow_rate.csv')
        with open(flow_rate_csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Nombre de Imagen", "Pixeles Horizontales", "Particulas Amarillas", "Particulas Azules"])

        for image in image_filename:
            frame_output_total_path = os.path.join(directory, image)
            mask_output_total_path = os.path.join(mask_folder, f'mask_output_{image}')
            output_frames_csv_path = os.path.join(directory, f'output-frames_{image}.csv')
            output_csv_path = os.path.join(csv_folder, f'output_{image}.csv')
            output_pdf_path = os.path.join(pdf_folder, f'output_{image}.pdf')

            Fullimage = cv2.imread(frame_output_total_path)
            num_yellow_contours, num_blue_contours = binarize_exit(
                Fullimage, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7],
                sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13]
            )

            # Leer las máscaras
            mask_yellow = cv2.imread(mask_output_total_path.replace('.jpg', '_yellow.png'), cv2.IMREAD_GRAYSCALE)
            mask_blue = cv2.imread(mask_output_total_path.replace('.jpg', '_blue.png'), cv2.IMREAD_GRAYSCALE)

            # Pintar píxeles detectados en imágenes originales
            yellow_detected_image = paint_detected_pixels(Fullimage, mask_yellow, (0, 255, 0), ancho_pixel_amarillo, alto_pixel_amarillo)  # Green color
            blue_detected_image = paint_detected_pixels(Fullimage, mask_blue, (0, 255, 0), ancho_pixel_azul, alto_pixel_azul)  # Green color

            # Guardar imágenes con píxeles detectados
            cv2.imwrite(os.path.join(original_detected_folder, f'yellow_detected_{image}'), yellow_detected_image)
            cv2.imwrite(os.path.join(original_detected_folder, f'blue_detected_{image}'), blue_detected_image)

            # Crear un archivo CSV para la información de la imagen si cumple con el criterio
            if num_yellow_contours >= min_contornos or num_blue_contours >= min_contornos:
                num_pixeles_horizontales = Fullimage.shape[1]
                with open(flow_rate_csv_path, mode='a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([image, num_pixeles_horizontales, num_yellow_contours, num_blue_contours])

    except Exception as e:
        print(f"Se produjo un error: {str(e)}")

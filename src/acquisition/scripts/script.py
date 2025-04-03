#!/usr/bin/env python3

import os
import gi
import sys
import cv2
import time
import pyfirmata
import numpy as np

from datetime import datetime
from combine_img import combine
from motor_control import motor1
from delete_files import eliminar, crear_directorio
from cut_video_frames import cut_video
from binarize_frame import color_particle
from generate_file_name import generate_file_name


gi.require_version("Tcam", "1.0")
gi.require_version("Gst", "1.0")
gi.require_version("GLib", "2.0")
from gi.repository import Tcam, Gst, GLib
global counter
counter = int(sys.argv[1])


def main(counter):
    '''
    Ejecuta el programa principal para grabar un video hasta que se cumpla una condición de finalización.

    Esta función realiza la grabación de un video utilizando una cámara configurada y analiza los frames,
    guardando el video resultante en un archivo AVI. El programa se ejecuta hasta que se cumple una condición de
    finalización, como alcanzar un límite de tiempo o detectar una condición específica. Al finalizar, se establece
    el estado del pipeline en "NULL" y se muestra la ubicación del video guardado.

    Requiere las siguientes configuraciones y componentes:
        - Cámara conectada y configurada.
        - Arduino conectado al puerto serie y los pines configurados correctamente.
        - Archivos importados disponibles en el mismo directorio.

    Parameters:
    counter (int): Un contador o identificador para la medición actual.

    Returns:
    int: 0 si el programa se ejecutó correctamente.
    '''
    
    # Variables globales
    global amp
    global yellow_counter
    yellow_counter = 0

    # Configuracion del puerto de la camara
    Gst.init(sys.argv)
    Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)
    serial = "12320143-aravis"

    # Configuracion parlante
    parlante.write(0)


    # FPS a los que se realiza la filmacion
    fps = 480

    # Tiempo maximo para una medicion en segundos
    tiempo = 600

    # Crear el pipeline 320 16
    pipeline = Gst.parse_launch(
        "tcambin name=source"
        " ! video/x-raw,format=BGRx,width=480,height=16,framerate=" +
        str(fps) + "/1"
        " ! videoconvert"
        " ! tee name=t"
        " t."
        " ! queue"
        " ! avimux"
        " ! filesink name=fsink"
        " t."
        " ! queue"
        " ! videoconvert"
        " ! appsink name=sink"
    )

    # Configurar la cámara
    source = pipeline.get_by_name("source")
    source.set_property("serial", serial)

    # Configurar el destino de archivo AVI
    fsink = pipeline.get_by_name("fsink")

    # Genera un nombre para el video
    file_location = generate_file_name(counter)
    fsink.set_property("location", file_location)

    # Configurar el elemento appsink para recibir señales y conectar la señal "new-sample"
    appsink = pipeline.get_by_name("sink")
    appsink.set_property("emit-signals", True)
    appsink.set_property("sync", False)
    appsink.connect("new-sample", on_new_sample)

    # Iniciar el pipeline y esperar a que la cámara esté en READY
    start_time_video = time.time()
    pipeline.set_state(Gst.State.READY)

    # Desactivar balance de blancos automático y establecerlo en modo manual
    source.set_tcam_enumeration("ExposureAuto", "Off")
    source.set_tcam_enumeration("GainAuto", "Off")
    #source.set_tcam_float("ExposureTime", float(1/(fps*2)))#4166.5999999999994543) # en que afecta?

    # Enciendo el parlante
    parlante.write(1)
    
    # Iniciar el pipeline para comenzar a filmar
    pipeline.set_state(Gst.State.PLAYING)

    # Comienza el ciclo de medicion
    

    try:
        # Segundos por la cantidad de FPS
        max_yellow_count = tiempo * fps #132266 # 

        while True:
            time.sleep(1)

            if yellow_counter >= max_yellow_count or arduino.digital[8].read() == False or arduino.digital[8].read() == None:
                # Si se llego al limite de tiempo o se detecta un vacio se rompe el bucle
                break

    except KeyboardInterrupt:
        
        pass

    finally:

        # Establecer el estado del pipeline en "NULL" para liberar recursos
        pipeline.set_state(Gst.State.NULL)
 

    end_time_video = time.time()
    

    # Interrumpo la perturbacion, apagando el parlante
    parlante.write(0)

    # Creo las carpetas necesarias
    today = datetime.today()
    folder_name = today.strftime("%d-%m-%Y")
    folder_path = os.path.join(
        "/home/juli/Documentos/Mediciones", folder_name)
    folder_path_frames = os.path.join(folder_path, "frames")

    # Corto el video
    start_time_cut = time.time()
    cut_video(file_location, folder_path_frames)
    #eliminar(file_location)
    end_time_cut = time.time()
    

    # Elimino archivos innecesarios
    start_time_combine = time.time()
    combine(counter, folder_path)
    eliminar(folder_path_frames)
    end_time_combine = time.time()

    # Creo nuevamente la carpeta frames
    crear_directorio(folder_path_frames)

    # Recarga de partículas 
    motor1(IN1, IN2, IN3, IN4, parlante)
    time.sleep(0.5)
    parlante.write(1)
    time.sleep(1)
    motor1(IN4, IN3, IN2, IN1, parlante)    
    
    # Calculo los tiempos de procesamiento, para referencia
    execution_time_video = end_time_video - start_time_video
    execution_time_cut = end_time_cut - start_time_cut
    execution_time_combine = end_time_combine - start_time_combine
 
    return 0


def on_new_sample(sink):
    """
    Callback para el elemento appsink que se ejecuta cuando hay una nueva muestra disponible.

    Args:
        sink: Elemento appsink.

    Returns:
        Gst.FlowReturn.OK: Si la operación se completó correctamente.
        Gst.FlowReturn.ERROR: Si hubo un error en la operación.
    """

    # Obtener la muestra del elemento appsink
    sample = sink.emit("pull-sample")

    global yellow_counter

    if sample:
        # Obtener el buffer de la muestra y las capacidades
        buffer = sample.get_buffer()

        if buffer:
            # Mapear los datos del buffer
            success, info = buffer.map(Gst.MapFlags.READ)
            caps = sample.get_caps()

            if success:
                # Acceder a los datos mapeados
                data = info.data
                structure = caps.get_structure(0)
                width = structure.get_value("width")
                height = structure.get_value("height")

                # Crear una matriz NumPy
                data_array = np.ndarray(
                    shape=(buffer.get_size(),), dtype=np.uint8, buffer=data)

                # Reshape y decodificar los datos en una matriz de imagen
                image = np.reshape(data_array, (height, width, 4))
                image_bgr = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

                # Analizar si hay amarillo
                particle = color_particle(image_bgr)

                if not particle:
                    yellow_counter += 1
                else:
                    yellow_counter = 0
                # Desmapear el buffer después de usarlo
                buffer.unmap(info)

        return Gst.FlowReturn.OK

    else:

        return Gst.FlowReturn.ERROR


def print_properties(camera):
    """
    Print selected properties
    """
    try:
        property_exposure_auto = camera.get_tcam_property("ExposureAuto")
        print(property_exposure_auto.get_value())
        value = camera.get_tcam_enumeration("ExposureAuto")
        print(f"Exposure Auto has value: {value}")
        value = camera.get_tcam_enumeration("GainAuto")
        print("Gain Auto has value: {}".format(value))
        value = camera.get_tcam_float("ExposureTime")
        print("ExposureTimer has value: {}".format(value))
    except GLib.Error as err:
        print(f"{err.message}")


if __name__ == "__main__":

    today = datetime.today()
    folder_name = today.strftime("%d-%m-%Y")
    
    # Configuración del puerto serie
    puerto_serie = '/dev/ttyUSB0'
    arduino = pyfirmata.Arduino(puerto_serie)
    time.sleep(1)

    # Configurar los pines como entrada o salida
    IN1 = arduino.get_pin('d:4:o')
    IN2 = arduino.get_pin('d:5:o')
    IN3 = arduino.get_pin('d:6:o')
    IN4 = arduino.get_pin('d:7:o')
    proximidad = arduino.get_pin('d:8:i')
    parlante = arduino.get_pin('d:9:o')
    
    # Inicializo el Arduino UNO
    it = pyfirmata.util.Iterator(arduino)
    it.start()
    arduino.digital[8].enable_reporting()
    
    
    # Esta parte es importante para que cuando el motor se mueva no se trabe ni nada, porque ya estan energizadas las bobinas iniciales
    IN1.write(0)
    IN2.write(0)
    IN3.write(1)
    IN4.write(1)

    if len(sys.argv) > 1:
        for i in range(counter):
            main(i)
    else:
        print("Error: Falta argumentos")

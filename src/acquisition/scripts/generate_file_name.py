#!/usr/bin/env python3
import os
from datetime import datetime


def generate_file_name(counter):
    """
    Genera un nombre de archivo único para el video.

    Returns:
        str: Nombre de archivo generado.
    """
    counter
    
    today = datetime.today()
    folder_name = today.strftime("%d-%m-%Y")
    folder_path = os.path.join("/media/juli/BACKUP-1", folder_name)
    #folder_frames = os.path.join(folder_path, "frames")
    
    
    os.makedirs(folder_path, exist_ok=True)
    #os.makedirs(folder_frames, exist_ok=True)
    
    
    file_name = f"video_{counter}.avi"

    file_path = os.path.join(folder_path, file_name)

    return file_path

if __name__ == '__main__':
    generate_file_name()

#!/bin/bash

# Limpiar archivos anteriores
rm -r post
rm restart*
rm poly*
rm log.liggghts
rm *.csv
rm *.stl
clear

# Crea las mallas
python3 generate_mesh.py
clear

# Ejecutar simulación de LIGGGHTS en segundo plano y capturar su PID
time liggghts -in input.liggghts
#time mpirun -np 4 liggghts < input.liggghts

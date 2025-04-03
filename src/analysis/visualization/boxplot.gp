#!/bin/usr/gnuplot   
# Este script de Gnuplot genera un gráfico de tipo boxplot a partir de un archivo CSV de datos.
# El usuario puede especificar el nombre del archivo CSV que desea plotear cuando se ejecuta el script.
# El script solicitará al usuario que ingrese el nombre del archivo deseado, incluyendo la ruta si es necesario.
# Luego, el script generará un archivo de imagen PNG con el nombre proporcionado por el usuario y mostrará el boxplot correspondiente.
# La configuración del boxplot incluye la eliminación de los valores atípicos, un ancho de línea de mediana de 2.5 y un estilo de relleno sólido con un borde definido.
# Se recomienda modificar la configuración de estilo, como el color, según las preferencias del usuario.



set terminal png
set datafile separator ","
set style boxplot nooutliers medianlinewidth 2.5
set style fill solid 0.25 border -1

# Pedir al usuario el nombre del archivo
print "Ingrese el nombre del archivo a plotear (incluyendo la ruta si es necesario):"
read filename

# Salida con nombre dinámico basado en el nombre del archivo
set output filename . '.png'

# Plotear el archivo ingresado por el usuario
plot filename using (1):5 with boxplot lc rgb "blue"

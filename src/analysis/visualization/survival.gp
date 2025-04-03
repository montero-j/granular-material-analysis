#!/bin/usr/gnuplot   

# Este script de Gnuplot genera un gráfico en formato PDF a partir de un archivo de datos. 
# El usuario puede especificar el nombre y la ubicación del archivo de datos que desea plotear cuando se ejecuta el script.
# El script solicitará al usuario que ingrese el nombre del archivo deseado, incluyendo la ruta si es necesario.
# Luego, el script generará un archivo de imagen PDF con el nombre proporcionado por el usuario y mostrará el gráfico correspondiente.
# La configuración del gráfico incluye un eje x y un eje y con etiquetas personalizadas, así como una escala logarítmica en ambos ejes.
# Se ha definido un rango específico para los valores de y y x, y se ha ajustado el estilo de las etiquetas y el margen del gráfico.
# Se recomienda modificar la configuración según las preferencias del usuario, como el título, la escala de los ejes o el estilo de las líneas y puntos.

set terminal pdf
set log xy

# Pedir al usuario el nombre del archivo de salida
print "Ingrese el nombre del archivo de salida (sin extensión):"
read filename

set output filename . '.pdf'

# Configuración del gráfico
set xlabel '{/Symbol t} (s)' font ",25"
set ylabel 'P (T > {/Symbol t})' font ",25" offset -2,0
set ytics font ", 25"
set xtics font ", 25"
set key font ",20"
set bmargin 5
set lmargin 13
set rmargin 5
set yrange[0.0005:1]
set xrange[:1200]

# Plotear el archivo ingresado por el usuario
plot filename title "" w points pt 7 ps 0.5


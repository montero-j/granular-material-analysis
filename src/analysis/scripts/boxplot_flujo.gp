# Establecer estilo y formato de los gráficos
set terminal pngcairo enhanced font 'arial,10' size 800, 600
set output 'boxplot_flujo_particulas_amarillas.png'

# Definir las etiquetas de los datos
set style data boxplot
set xtics nomirror rotate by -45 scale 0

# Título y etiquetas de los ejes
set title "Boxplot del Flujo de Partículas Amarillas"
set xlabel "Flujo Partículas Amarillas"
set ylabel "Cantidad"

# Definir los datos a graficar y su formato
plot 'datos.csv' using (1):($4) title 'Flujo Partículas Amarillas'

#!/bin/usr/gnuplot   
set terminal png size 1024,768
set output "data.png"

cd 'C:\Users\usuario\OneDrive\Documentos\Trabajo\Congresos\RAFA_2023\poster\imagen_poster'
set datafile separator ","
set multiplot
set size 1.0,1.0
set yrange[-0.05:1.05]
set xrange[325:740]
set ytics 0,1,1
#set xlabel 'Frames' font ",20"
#set ylabel 'Flujo de descarga' font ",20"

set ytics font ", 20"
set xtics font ", 20"
set xtics offset 0,-0.5

plot "output_frame_output_medicion_26_1.jpg_yellow.csv" using ($1/600):($2) w lines ls 6 lw 2 title ""
set size 0.4, 0.5
set origin 0.6, 0.5
set xtics 490,10,505
set ylabel ""
set xlabel ""
plot [490:505]"output_frame_output_medicion_26_1.jpg_yellow.csv" using ($1/600):($2) w lines ls 6 lw 2 title ""
unset multiplot

#!/bin/usr/gnuplot   
set log xy
set datafile separator ","

plot "~/Documentos/gfsg/experimentos/atascamiento/2024/05-04-2024/data/data_yellow.csv" title "05-04 - H=58% - A=320mV" pt 7, "~/Documentos/gfsg/experimentos/atascamiento/2024/08-04-2024/data/data_yellow.csv" title "08-04 - H=70% - A=320mV" pt 7, "~/Documentos/gfsg/experimentos/atascamiento/2024/21-03-2024/data/data_yellow.csv" title "21-03 - H=70% - A=200mV" pt 7, "~/Documentos/gfsg/experimentos/atascamiento/2024/22-03-2024/data/data_yellow.csv"title "22-03 - H=50% - A=200mV" pt 7, "~/Documentos/gfsg/experimentos/atascamiento/2024/27-03-2024/data/data_yellow.csv" title "27-03 - H=74% - A=240mV" pt 7, "~/Documentos/gfsg/experimentos/atascamiento/2024/09-04-2024/data/data_yellow.csv" title "09-04 - H=66% - A=320mV" pt 7

pause -1
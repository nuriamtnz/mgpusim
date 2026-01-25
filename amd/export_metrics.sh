#!/bin/bash

cd ~/tfg/mgpusim/results_prefetch

#creación de fichero y escribir cabecera de columnas
echo "benchmark,mode,Location,What,Value,Unit" > summary_metrics.csv

#bucle
for b in */; do
  bench_name=${b%/}
  cd "$bench_name"
  for db in metrics_*.sqlite3; do
    mode=${db#metrics_} #elimina prefijo "metrics_"
    mode=${mode%.sqlite3} #elimina sufijo ".sqlite3"
    sqlite3 -csv "$db" \
      "SELECT '$bench_name','$mode',Location,What,Value,Unit FROM mgpusim_metrics;" \
      >> ../summary_metrics.csv
  done
  cd ..
done

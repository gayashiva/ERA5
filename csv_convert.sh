#!/bin/bash
for f in results/leh/*.grib
do 
#  out = "csv/"
  echo "results/leh/csv/$(basename ${f%.*}.csv)"
  grib_get_data -p dataDate,shortName,validityTime "$f"> "results/leh/csv/$(basename ${f%.*}.csv)"
done

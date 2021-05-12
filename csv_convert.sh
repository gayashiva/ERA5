#!/bin/bash
for f in results/diavolezza/*.grib
do 
#  out = "csv/"
  echo "results/diavolezza/csv/$(basename ${f%.*}.csv)"
  grib_get_data -p dataDate,shortName,validityTime "$f"> "results/diavolezza/csv/$(basename ${f%.*}.csv)"
done

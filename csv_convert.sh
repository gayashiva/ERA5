#!/bin/bash
for f in results/guttannen/*.grib
do 
#  out = "csv/"
  echo "results/guttannen/csv/$(basename ${f%.*}.csv)"
  grib_get_data -p dataDate,shortName,validityTime "$f"> "results/guttannen/csv/$(basename ${f%.*}.csv)"
done

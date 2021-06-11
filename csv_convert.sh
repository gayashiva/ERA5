#!/bin/bash
for f in results/ravat/*.grib
do 
#  out = "csv/"
  echo "results/ravat/csv/$(basename ${f%.*}.csv)"
  grib_get_data -p dataDate,shortName,validityTime "$f"> "results/ravat/csv/$(basename ${f%.*}.csv)"
done

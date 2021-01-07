#!/bin/bash
for f in results/schwarzsee/*.grib
do 
#  out = "csv/"
  echo "results/schwarzsee/csv/$(basename ${f%.*}.csv)"
  grib_get_data -p dataDate,shortName,validityTime "$f"> "results/schwarzsee/csv/$(basename ${f%.*}.csv)"
done

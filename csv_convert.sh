#!/bin/bash
loc="altiplano"
for f in results/"$loc"/*.grib
do 
#  out="csv/"
  echo "results/$loc/csv/$(basename ${f%.*}.csv)"
  grib_get_data -p dataDate,shortName,validityTime "$f" > "results/$loc/csv/$(basename ${f%.*}.csv)"
done

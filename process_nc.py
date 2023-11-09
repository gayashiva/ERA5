import pandas as pd
import xarray as xr
import os, shutil
import numpy as np
from datetime import datetime, timedelta
import os
import json

def get_percentage_missing(series):
    """ Calculates percentage of NaN values in DataFrame
    :param series: Pandas DataFrame object
    :return: float
    """
    num = series.isnull().sum()
    den = len(series)
    return round(num/den, 2)

def e_sat(T, surface="water", a1=611.21, a3=17.502, a4=32.19):
    T += 273.16
    if surface == "ice":
        a1 = 611.21  # Pa
        a3 = 22.587  # NA
        a4 = -0.7  # K
    return a1 * np.exp(a3 * (T - 273.16) / (T - a4))

# locations = ["schwarzsee", "leh", "guttannen", "diavolezza"]
locations = ["leh"]
coords = (34.216638,77.606949)
# locations = ["north_america", "europe", "south_america", "central_asia"]
years = ["2019", "2020"]

# reading the data from the file
with open("/home/bsurya/Projects/AIR-Zones/output/max_region_coords.json") as f:
    locs = f.read()

# # reconstructing the data as a dictionary
# locs = json.loads(locs)

# for loc, coords in locs.items():
for loc in locations:
    for when in years:
        print(loc, when)

    # print(str(value[0] - 0.05) + "/" + str(value[1] - 0.05) +"/"+str(value[0] + 0.05) + "/" +str(value[1] +0.05))

# locations = ["south_america", "europe", "north_america", "central_asia"]
# locations = ["schwarzsee", "guttannen", "diavolezza"]
# for loc in locations:
    # for when in years:
        # print(loc)
        # when = "2019"
        os.chdir("/home/bsurya/Projects/ERA5/results/" + loc + "/")

        da = xr.open_mfdataset("*.nc", parallel=True)
        # da = da.sel(latitude=coords[0], longitude=coords[1], method='nearest')
        # print(da.v10)
        # df = da.sel(time=when).t2m.to_dataframe()
        df = da.sel(time=when).to_dataframe()
        print(df.head())
        df = df.reset_index()

        # Process data for ERA5

        df.to_csv( "/home/bsurya/Projects/ERA5/outputs/" + loc + "_" + when + ".csv")

        # da.close()

        # da = xr.open_mfdataset("era5_tcc_year_2022_reanalysis-era5-single-levels.nc", parallel=True)
        # df = da.sel(time=when, expver=1).to_dataframe()
        # df = df.reset_index()
        # df = df.set_index("time")
        # df = df.drop(['longitude', 'latitude', 'expver'], axis=1)
        # df = df.dropna(axis=1, how='all')
        # print(df.describe())
        # print(get_percentage_missing(df["tcc"]))


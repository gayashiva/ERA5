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

locations = ["leh", "north_america", "europe", "south_america", "central_asia"]
# reading the data from the file
with open("/home/bsurya/Projects/AIR-Zones/output/max_region_coords.json") as f:
    sites = f.read()
# reconstructing the data as a dictionary
sites = json.loads(sites)
years = ["2019", "2020"]

for loc in locations:
    for when in years:
        print()
        print(loc, when)
        os.chdir("/home/bsurya/Projects/ERA5/results/" + loc + "/")

        da = xr.open_mfdataset("*.nc", parallel=True)
        da = da.sel(latitude=sites[loc][0], longitude=sites[loc][1], method='nearest')
        df = da.sel(time=when).to_dataframe()
        df = df.drop(['longitude', 'latitude'], axis=1)
        print(df.head())
        # df = df.reset_index()

        # Process data for ERA5
        df.to_csv( "/home/bsurya/Projects/ERA5/outputs/" + loc + "_" + when + ".csv")

    df1= pd.read_csv(
        "/home/bsurya/Projects/ERA5/outputs/" + loc + "_2019.csv",
        sep=",",
        header=0,
        parse_dates=["time"],
    )
    df2= pd.read_csv(
        "/home/bsurya/Projects/ERA5/outputs/" + loc + "_2020.csv",
        sep=",",
        header=0,
        parse_dates=["time"],
    )
    # Combine DataFrames
    df3 = pd.concat([df1, df2])
    df3['time'] = pd.to_datetime(df3['time'])
    df3.to_csv( "/home/bsurya/Projects/air_model/data/era5/" + loc + "20" + ".csv")

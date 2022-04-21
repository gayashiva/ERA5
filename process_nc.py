import pandas as pd
import xarray as xr
import os, shutil
import numpy as np
from datetime import datetime, timedelta
import os
import re

def get_percentage_missing(series):
    """ Calculates percentage of NaN values in DataFrame
    :param series: Pandas DataFrame object
    :return: float
    """
    num = series.isnull().sum()
    den = len(series)
    return round(num/den, 2)

# locations = ["schwarzsee", "leh", "guttannen", "diavolezza"]
# locations = ["leh", "guttannen"]
locations = ["guttannen"]
# locations = ["schwarzsee", "guttannen", "diavolezza"]
for loc in locations:
    print(loc)
    when = "2022"
    os.chdir("/home/suryab/work/ERA5/results/" + loc + "/")

    da = xr.open_mfdataset("*.nc", parallel=True)
    # df = da.sel(time=when, expver=1).tcc.to_dataframe()
    df = da.sel(time=when, expver=1).to_dataframe()
    df = df.reset_index()
    df = df.set_index("time")
    df = df.drop(['longitude', 'latitude', 'expver'], axis=1)
    df = df.dropna(axis=1, how='all')
    print(df.describe())
    print(df.head())
    print(df.tail(20))

    df.to_csv( "/home/suryab/work/ERA5/outputs/" + loc + "_" + when + ".csv")

    da.close()

    da = xr.open_mfdataset("era5_t2m_year_2022_reanalysis-era5-single-levels.nc", parallel=True)
    df = da.sel(time=when, expver=1).to_dataframe()
    df = df.reset_index()
    df = df.set_index("time")
    df = df.drop(['longitude', 'latitude', 'expver'], axis=1)
    df = df.dropna(axis=1, how='all')
    print(df.describe())
    print(get_percentage_missing(df["t2m"]))


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

def e_sat(T, surface="water", a1=611.21, a3=17.502, a4=32.19):
    T += 273.16
    if surface == "ice":
        a1 = 611.21  # Pa
        a3 = 22.587  # NA
        a4 = -0.7  # K
    return a1 * np.exp(a3 * (T - 273.16) / (T - a4))

# locations = ["schwarzsee", "leh", "guttannen", "diavolezza"]
# locations = ["leh", "guttannen"]
locations = ["altiplano"]
coords = (-17.14375, -69.997917)
# locations = ["schwarzsee", "guttannen", "diavolezza"]
for loc in locations:
    print(loc)
    when = "2020"
    os.chdir("/home/bsurya/Projects/ERA5/results/" + loc + "/")

    # da = xr.open_mfdataset("era5_t2m_year_2019_reanalysis-era5-land.nc", parallel=True)
    da = xr.open_mfdataset("*.nc", parallel=True)
    da = da.sel(latitude=coords[0], longitude=coords[1], method='nearest')
    # df = da.sel(time=when).t2m.to_dataframe()
    df = da.sel(time=when).to_dataframe()
    df = df.reset_index()
    df = df.set_index("time")

    time_steps = 60 * 60
    df["ssrd"] /= time_steps
    df["strd"] /= time_steps
    df['wind'] = np.sqrt(df.u10**2 + df.v10**2)
    # df["tp"] = df["tp"] * 1000  # mm
    # Derive RH
    df["t2m"] -= 273.15
    df["d2m"] -= 273.15
    df["t2m_RH"] = df["t2m"].copy()
    df["d2m_RH"] = df["d2m"].copy()
    df= df.apply(lambda x: e_sat(x) if x.name == "t2m_RH" else x)
    df= df.apply(lambda x: e_sat(x) if x.name == "d2m_RH" else x)
    df["RH"] = 100 * df["d2m_RH"] / df["t2m_RH"]
    df["sp"] = df["sp"] / 100
    df = df.drop(['longitude', 'latitude', 'u10', 'v10', 't2m_RH', 'd2m_RH', 'd2m'], axis=1)
    df = df.reset_index()
    # CSV output
    df.rename(
        columns={
            "time": "TIMESTAMP",
            "t2m": "temp",
            "sp": "press",
            "tp": "ppt",
            "ssrd": "SW_global",
            "fdir": "SW_direct",
            "strd": "LW_in",
        },
        inplace=True,
    )
    df = df.dropna(axis=1, how='all')
    df = df.round(3)
    print(df.columns)
    print(df.describe())
    print(df.head())
    print(df.tail(20))

    # Process data for ERA5

    df.to_csv( "/home/bsurya/Projects/ERA5/outputs/" + loc + "_" + when + ".csv")

    da.close()

    # da = xr.open_mfdataset("era5_tcc_year_2022_reanalysis-era5-single-levels.nc", parallel=True)
    # df = da.sel(time=when, expver=1).to_dataframe()
    # df = df.reset_index()
    # df = df.set_index("time")
    # df = df.drop(['longitude', 'latitude', 'expver'], axis=1)
    # df = df.dropna(axis=1, how='all')
    # print(df.describe())
    # print(get_percentage_missing(df["tcc"]))


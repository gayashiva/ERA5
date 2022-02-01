import pandas as pd
import xarray as xr
import os, shutil
import numpy as np
from datetime import datetime, timedelta
import os
import re


# locations = ["schwarzsee", "leh", "guttannen", "diavolezza"]
# locations = ["leh", "guttannen"]
locations = ["guttannen"]
# locations = ["schwarzsee", "guttannen", "diavolezza"]
for loc in locations:
    print(loc)
    when = "2021"
    os.chdir("/home/suryab/work/ERA5/results/" + loc + "/")

    da = xr.open_mfdataset("*.nc", parallel=True)
    # df = da.sel(time=when, expver=1).tcc.to_dataframe()
    df = da.sel(time=when, expver=1).to_dataframe()
    df = df.reset_index()
    df = df.set_index("time")
    df = df.drop(['longitude', 'latitude', 'expver'], axis=1)
    print(df.describe())
    print(df)

    df.to_csv( "/home/suryab/work/ERA5/outputs/" + loc + "_" + when + ".csv")

    da.close()

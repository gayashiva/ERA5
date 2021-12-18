import pandas as pd
import xarray as xr
import os, shutil
import numpy as np
from datetime import datetime, timedelta
import os
import re


# locations = ["schwarzsee", "leh", "guttannen", "diavolezza"]
locations = ["leh", "guttannen"]
# locations = ["schwarzsee", "guttannen", "diavolezza"]
for loc in locations:
    print(loc)
    when = "2021"
    os.chdir("/home/suryab/work/ERA5/results/" + loc + "/")

    da = xr.open_mfdataset("*.nc", parallel=True)
    df = da.sel(time=when, expver=1).tcc.to_dataframe()
    print(df.describe())

    # df = da.sel(time=when, expver=1).to_dataframe()
    # df["t2m"] -= 273.15
    # print(df.t2m.describe())
    # df.to_netcdf("../" + loc + "-" + when + ".nc")
    da.close()
    # df.close()

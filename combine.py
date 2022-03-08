import pandas as pd
import os, shutil
import numpy as np
from datetime import datetime, timedelta
import os
import re

# locations = ["schwarzsee", "leh", "guttannen", "diavolezza"]
locations = ["guttannen"]
# locations = ["leh"]
compile = "True"
for site in locations:
    # years = ["2019", "2020", "2021"]
    years = ["2021", "2022"]
    os.chdir("/home/suryab/work/ERA5/results/" + site + "/")

    if compile == "True":
        if not os.path.exists("csv/output"):
            os.mkdir("csv/output")
        else:
            # Delete folder contents
            folder = "csv/output"
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))
        # Create new files
        os.chdir("csv/")
        directory = os.listdir()
        for file in directory:
            var = re.split("[.|_]", file)
            for year in years:
                if not os.path.exists("output/" + year):
                    os.mkdir("output/" + year)
                x = re.search(year, file)
                if x:
                    if len(var) == 6:
                        filename = var[1] + "_" + var[4]
                        with open(file, "r") as f_in, open(
                            "output/" + year + "/" + filename + ".csv", "w"
                        ) as f_out:
                            f_out.write(next(f_in).replace(" ", ""))
                            i = 0
                            for line in f_in:
                                if i % 2 == 0:
                                    f_out.write(",".join(line.split()) + "\n")
                                i = i + 1
                    else:
                        filename = var[1]
                        with open(file, "r") as f_in, open(
                            "output/" + year + "/" + filename + ".csv", "w"
                        ) as f_out:
                            f_out.write(next(f_in).replace(" ", ""))
                            i = 0
                            for line in f_in:
                                if i % 2 == 0:
                                    f_out.write(",".join(line.split()) + "\n")
                                i = i + 1

    # ERA5 begins
    for year in years:
        begin = datetime(int(year), 1, 1)
        stop = datetime(int(year), 12, 31, 23)
        days = pd.date_range(start=begin, end=stop, freq="1H")
        df_merged = pd.DataFrame({"When": days})
        directory = os.listdir("output/" + year)
        print(directory)
        # os.chdir("output/" + year)
        l = ["When"]
        for file in directory:
            var = re.split("[.|_]", file)
            l.append(var[0])
            df_in = pd.read_csv("output/" + year + "/" + file, sep=",", header=0)
            df_in = df_in.drop(
                ["Latitude", "Longitude", "shortName", "dataDate", "validityTime"],
                axis=1,
            )
            df_in = df_in.reset_index()
            df_merged = df_merged.merge(
                df_in, how="outer", left_index=True, right_index=True
            )
            df_merged.rename(
                columns={
                    "Value": var[0],
                },
                inplace=True,
            )
        df_merged = df_merged[l]
        print(df_merged.tail())
        if df_merged.isnull().values.any():
            print("Warning: Null values present")
        else:
            print("No Errors")
        df_merged.to_csv("/home/suryab/work/ERA5/outputs/" + site + "_" + year + ".csv")
# df_merged.to_csv(
#     "/home/suryab/work/air_model/data/" + site + "/raw/ERA5_" + site + ".csv"
# )
# RMSE
# print("RMSE Temp", ((df_merged.T_a - df_merged.T_a<) ** 2).mean() ** 0.5)


# slope, intercept, r_value1, p_value, std_err = stats.linregress(
#     df.T_a.values, df_in3.T_a.values
# )
# slope, intercept, r_value2, p_value, std_err = stats.linregress(
#     df.v_a.values, df_in3.v_a.values
# )

# print("R2 temp", r_value1 ** 2)
# print("R2 wind", r_value2 ** 2)

import pandas as pd
import os, shutil
import numpy as np
from datetime import datetime, timedelta
import os
import re

site = "schwarzsee"
compile = "False"
os.chdir("results/" + site + "/csv")
begin = datetime(2019, 1, 1)
stop = datetime(2019, 12, 31, 23)
days = pd.date_range(start=begin, end=stop, freq="1H")
df_merged = pd.DataFrame({"When": days})

if compile == "True":
    # Delete folder contents
    folder = "output"
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
    directory = os.listdir()
    for file in directory:
        var = re.split("[.|_]", file)
        x = re.search("2019", file)
        if x:
            if len(var) == 6:
                filename = var[1] + "_" + var[4]
                with open(file, "r") as f_in, open(
                    "output/" + filename + ".csv", "w"
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
                    "output/" + filename + ".csv", "w"
                ) as f_out:
                    f_out.write(next(f_in).replace(" ", ""))
                    i = 0
                    for line in f_in:
                        if i % 2 == 0:
                            f_out.write(",".join(line.split()) + "\n")
                        i = i + 1

# ERA5 begins
directory = os.listdir("output")
os.chdir("output")
l = ["When"]
for file in directory:
    var = re.split("[.|_]", file)
    print(var[0])
    l.append(var[0])
    df_in = pd.read_csv(file, sep=",", header=0)
    print(file)
    df_in = df_in.drop(
        ["Latitude", "Longitude", "shortName", "dataDate", "validityTime"], axis=1
    )
    df_in = df_in.reset_index()
    df_merged = df_merged.merge(df_in, how="outer", left_index=True, right_index=True)
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
df_merged.to_csv(
    "/home/surya/Programs/Github/air_model/data/" + site + "/raw/ERA5_" + site + ".csv"
)
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

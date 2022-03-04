import numpy as np
import pandas as pd


def import_data(file_name):
    # Read CSV data into pandas dataframe
    df = pd.read_csv(file_name)

    # trim start and end of files
    trim_points = {
        "Data/L103/L1-03.csv": [44, -3],
        "Data/L104/L1-04.csv": [37, -5],
        "Data/L105/L1-05.csv": [38, -5],
        "Data/L109/L1-09.csv": [35, -4],
        "Data/L123/L1-23.csv": [814, -4878]
    }
    start = trim_points[file_name][0]                   # start of  useful data
    end = trim_points[file_name][1]                     # end of useful data
    df = df[start:end]                                  # trimmed data

    # Create new dataframe
    count = df["Count"]
    time = df["Time_0"]
    load = df["Dev2/ai0"] * 10
    displacement = df["Dev2/ai1"] * 0.75

    data_numpy = np.vstack((count, time, load, displacement)).transpose()
    data_columns = ["count", "time", "load", "displacement"]
    df_processed = pd.DataFrame(data=data_numpy, columns=data_columns)

    return df_processed




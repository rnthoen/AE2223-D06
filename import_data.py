import numpy as np
import pandas as pd


def import_data(file_names):
    """
    :param file_names: file_names[0] contains MTS data, remainder of file_names containts DTC files
    :return:    - df_processed_MTS is the MTS data with columns = ['count', 'time', 'load', 'displacement']
                - df_processed_DIC is the DIC data with columns = ['', 'x', 'y', 'z', 'u', 'v', 'w', 'Exx', 'Eyy', 'Exy', 'E1', 'E2']
    """

    # Read MTS CSV data into pandas dataframe
    df_MTS = pd.read_csv(file_names[0])

    # trim start and end of files
    trim_points = {
        "Data/L103/L1-03.csv": [44, -3],
        "Data/L104/L1-04.csv": [37, -5],
        "Data/L105/L1-05.csv": [38, -5],
        "Data/L109/L1-09.csv": [35, -4],
        "Data/L123/L1-23.csv": [814, -4878]
    }
    start = trim_points[file_names][0]                   # start of  useful data
    end = trim_points[file_names][1]                     # end of useful data
    df_MTS = df_MTS[start:end]                                  # trimmed data

    # Create new dataframe
    count = df_MTS["Count"]
    time = df_MTS["Time_0"]
    load = df_MTS["Dev2/ai0"] * 10
    displacement = df_MTS["Dev2/ai1"] * 0.75

    data_numpy = np.vstack((count, time, load, displacement)).transpose()
    data_columns = ["count", "time", "load", "displacement"]
    df_processed_MTS = pd.DataFrame(data=data_numpy, columns=data_columns)

    # read DIC CSV data into pandas dataframes



    return df_processed_MTS




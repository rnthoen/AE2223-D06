import pandas as pd
import numpy as np
from interpolate_panel import interpolate_panel

def lookup_DIC_data(cycle_number, df_separated, df_data, X_position, Y_position, column_type):

    # find start and end in df_separated for cycle_number
    idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number].index.tolist()
    start_count = int(df_separated.start_count[idx])
    end_count = int(df_separated.end_count[idx])

    # find load and strain for each point from start to end (both incl.)
    load_list = []
    column_position_list = []

    i = start_count
    while i <= end_count:
        if i%2 == 0:
            Column_position = interpolate_panel(df_data[1],i,X_position,Y_position,column_type)
            column_position_list.append(float(Column_position))

            idx = df_data[0]['count'][df_data[0]['count'] == i].index.tolist()
            load = float(df_data[0].load[idx])
            load_list.append(load)
        i += 1

    # format in a return array
    result = [cycle_number, load_list, column_position_list]

    return result

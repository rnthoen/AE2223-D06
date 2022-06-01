import pandas as pd
import matplotlib.pyplot as plt

def heatmap_data(cycle_number, count_offset, df_separated, df_data, variable):

    # find start and end in df_separated for cycle_number
    idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number].index.tolist()
    start_count = int(df_separated.start_count[idx])
    end_count = int(df_separated.end_count[idx])

    selected_count = start_count + count_offset
    if selected_count % 2 != 0:
        selected_count += 1
        print('count is not even, added 1 to print the next frame')
    if selected_count <= end_count:

        # find x and y for each point from start to end (both incl.)
        x_list = []
        y_list = []
        c_list = []

        indexes = df_data['File_Number'][df_data['File_Number'] == selected_count].index.tolist()

        for i in indexes:
            x = float(df_data['X'].iloc[i])
            y = float(df_data['Y'].iloc[i])
            c = float(df_data[variable].iloc[i])
            x_list.append(x)
            y_list.append(y)
            c_list.append(c)

        # format in a return array
        result = [x_list, y_list, c_list, cycle_number, selected_count]
        return result

    else:
        print('Invalid count_offset')

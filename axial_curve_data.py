import pandas as pd

# cycle_number_list is an array like [500, 1000, 1500]
# df_separated is the output of the separate_sequences() function
# df_data should look like "df_data[0]"

def axial_curve_data(cycle_number_list, df_separated, df_data):

    result = []
    for cycle_number in cycle_number_list:

        # find start and end in df_separated for cycle_number
        idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number].index.tolist()
        start_count = int(df_separated.start_count[idx])
        end_count = int(df_separated.end_count[idx])

        # find load and displacement for each point from start to end (both incl.)
        load_list = []
        displacement_list = []

        i = start_count
        while i <= end_count:
            idx = df_data['count'][df_data['count'] == i].index.tolist()
            load = float(df_data.load[idx])
            displacement = float(df_data.displacement[idx])
            load_list.append(load)
            displacement_list.append(displacement)
            i += 1

        # format in a return array
        result.append([cycle_number, load_list, displacement_list])

    return result

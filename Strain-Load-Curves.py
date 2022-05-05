import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from separate_sequences import separate_sequences
from import_data import import_data
from interpolate_panel import interpolate_panel

# cycle_number_list is an array like [500, 1000, 1500]
# df_separated is the output of the separate_sequences() function
# df_data should look like "df_data[0]"

files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840.csv', 'Data/L103/L1-03_8842_2_13994.csv', 'Data/L103/L1-03_13996_2_16696.csv'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160.csv', 'Data/L104/L1-04_4162_2_8548.csv', 'Data/L104/L1-04_8550_2_12242.csv', 'Data/L104/L1-04_12244_2_16402.csv', 'Data/L104/L1-04_16404_2_20098.csv', 'Data/L104/L1-04_20100_2_23800.csv', 'Data/L104/L1-04_23802_2_27262.csv', 'Data/L104/L1-04_27264_2_30036.csv', 'Data/L104/L1-04_30038_2_31422.csv'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050.csv', 'Data/L105/L1-05_4052_2_7978.csv', 'Data/L105/L1-05_7980_2_12136.csv', 'Data/L105/L1-05_12138_2_15722.csv'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016.csv', 'Data/L109/L1-09_4018_2_8288.csv', 'Data/L109/L1-09_8290_2_12072.csv', 'Data/L109/L1-09_12074_2_14760.csv'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000.csv', 'Data/L123/L1-23_4002_2_8080.csv', 'Data/L123/L1-23_8082_2_12430.csv', 'Data/L123/L1-23_12432_2_15850.csv', 'Data/L123/L1-23_15852_2_20506.csv', 'Data/L123/L1-23_20508_2_24236.csv', 'Data/L123/L1-23_24238_2_28894.csv', 'Data/L123/L1-23_28896_2_31384.csv', 'Data/L123/L1-23_31386_2_35416.csv', 'Data/L123/L1-23_35418_2_40390.csv', 'Data/L123/L1-23_40392_2_42256.csv']]

### Input space ###
## Select which specimen you want ##
select_specimen = files[3]

## Select which cycle numbers you want to see ##
cycle_number_list = [17000]

## Select position range of points to analyse strain for ##
x_middles = list(np.linspace(-70, 70, 10))
y_middles = list(np.linspace(0, 0, 10))

## Select which type of strain you want to analyse ##
column = "Exx"

### Imports MTS data and DIC data and sequences ###
df_data = import_data(select_specimen)

df_separated = separate_sequences(df_data[0])

### Beginning of strain-load curve data function ###
def strain_load_curve_data(cycle_number_list, df_separated, df_data, X_position, Y_position, column_type):

    result = []
    for cycle_number in cycle_number_list:
        for xs,X_middle in enumerate(X_position):
            #idx0 = X_position.index(xs)
            # find start and end in df_separated for cycle_number
            idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number].index.tolist()
            start_count = int(df_separated.start_count[idx])
            end_count = int(df_separated.end_count[idx])

            # find load and strain for each point from start to end (both incl.)
            load_list = []
            column_position_list = []

            i = start_count
            print(i)
            while i <= end_count:
                if i%2 == 0:
                    print(i)
                    Column_position = interpolate_panel(df_data[1],i,X_middle,Y_position[xs],column_type)
                    column_position_list.append(Column_position)

                    idx = df_data[0]['count'][df_data[0]['count'] == i].index.tolist()
                    load = float(df_data[0].load[idx])
                    load_list.append(load)
                i += 1

            # format in a return array
            result.append([cycle_number, load_list, column_position_list])

    return result

### Array with data. Shape = (number of cycles x number of positions) ###
plot_data = strain_load_curve_data(cycle_number_list, df_separated, df_data, x_middles, y_middles, column)

#print(plot_data[0][-1].iloc[0])
w_difference = []
for count,cycle_number in enumerate(cycle_number_list):
    for n in range(len(x_middles)):
        j = 1
        w_difference_list = []
        while j < len(plot_data[n+count*len(x_middles)][-1]):
            w_difference_list.append(plot_data[n+count*len(x_middles)][-1][j]-plot_data[n+count*len(x_middles)][-1][j-1])
            j += 1
        #w_difference_list = list(map(abs,w_difference_list))
        w_difference.append([cycle_number, w_difference_list])


### Several variables for labelling the right stuff ###
unit = ""
if column == "X" or column == "Y" or column == "Z" or column == "U" or column == "V" or column == "W":
    unit = "[mm]"
elif column == "Exx" or column == "Eyy" or column == "Exy" or column == "E1"  or column == "E2":
    unit = "[-]"

### Plot all locations for all cycle numbers ###
if len(cycle_number_list) == 1:
    fig, axs = plt.subplots(1, constrained_layout=True)
    for count, cycle in enumerate(cycle_number_list):
        for n in range(len(x_middles)):
            axs.plot(plot_data[n+count*len(x_middles)][1], plot_data[n+count*len(x_middles)][-1], label=f'{cycle} cycles at location (x={np.round(x_middles[n],2)},y={np.round(y_middles[n],2)})')
            new_load_list = plot_data[n+count*len(x_middles)][1].copy()
            new_load_list.pop(0)
            #axs.plot(new_load_list, w_difference[n+count*len(x_middles)][1], label=f'{cycle} cycles at location (x={np.round(x_middles[n], 2)},y={np.round(y_middles[n], 2)})')

            # axs[count].set_title(f'{column} at x = {np.round(x_middles,2)}, y = {np.round(y_middles,2)} vs. Load')
            axs.legend(bbox_to_anchor=(1.04, 1), loc="upper left", prop={'size': 5})
        axs.invert_xaxis()
        axs.invert_yaxis()

    axs.set(xlabel='Load [kN]', ylabel=f'{column} {unit}')
    fig.suptitle(f'{column}-Load Analysis of {select_specimen[0][5:9]}')
    plt.show()
else:
    fig, axs = plt.subplots(len(cycle_number_list),constrained_layout=True)
    for count, cycle in enumerate(cycle_number_list):
        for n in range(len(x_middles)):
            axs[count].plot(plot_data[n+count*len(x_middles)][1], plot_data[n+count*len(x_middles)][-1], label=f'{cycle} cycles at location (x={np.round(x_middles[n],2)},y={np.round(y_middles[n],2)})')
            new_load_list = plot_data[n+count*len(x_middles)][1].copy()
            new_load_list.pop(0)
            #axs[count].plot(new_load_list, w_difference[n+count*len(x_middles)][1], label=f'{cycle} cycles at location (x={np.round(x_middles[n],2)},y={np.round(y_middles[n],2)})')

            #axs[count].set_title(f'{column} at x = {np.round(x_middles,2)}, y = {np.round(y_middles,2)} vs. Load')
            axs[count].hlines(0.1, min(plot_data[n + count * len(x_middles)][1]),
                              max(plot_data[n + count * len(x_middles)][1]))
            axs[count].legend(bbox_to_anchor=(1.04, 1), loc="upper left", prop={'size': 5})
        axs[count].invert_xaxis()
        axs[count].invert_yaxis()

    for ax in axs.flat:
        ax.set(xlabel='Load [kN]', ylabel=f'{column} {unit}')

    fig.suptitle(f'{column}-Load Analysis of {select_specimen[0][5:9]}')
    plt.show()

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
if select_specimen == files[0]:
    specimen = "L103"
elif select_specimen == files[1]:
    specimen = "L104"
elif select_specimen == files[2]:
    specimen = "L105"
elif select_specimen == files[3]:
    specimen = "L109"
else: specimen = "L123"

## Select which cycle numbers you want to see ##
cycle_number_list = [17500]

### Imports MTS data and DIC data and sequences ###
df_data = import_data(select_specimen)
#df_data[1].to_csv(f'Data/Ben.csv')
df_separated = separate_sequences(df_data[0])

### Define variables ###
nu = 0.33
E = 1

#print(df_data[1])

### Find start and end in df_separated for cycle_number ###
# for cycle_number in cycle_number_list:
#     idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number].index.tolist()
#     start_count = int(df_separated.start_count[idx])
#     end_count = int(df_separated.end_count[idx])
#     total_count = end_count - start_count
#     real_count = int(total_count/10)
#     i = start_count
#     #print(i)
#     while i < end_count:
#         if i%2 == 0:
#             e_x_idx = df_data[1]['Exx'][df_data[1]['File_Number'] == i].index.tolist()
#
#             # print(e_x_idx)
#             # print(df_data[1]['Exx'][df_data[1]['File_Number'] == i])
#             # print(i)
#             e_x_list.append(df_data[1].Exx[e_x_idx])
#             e_y_idx = df_data[1]['Eyy'][df_data[1]['File_Number'] == i].index.tolist()
#             e_y_list.append(df_data[1].Eyy[e_y_idx])
#         i += 1
#     # print(e_x_list)
#     # print(e_y_list)

idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number_list[0]].index.tolist()
start_count = int(df_separated.start_count[idx])
if start_count%2 != 0:
    start_count += 1
end_count = int(df_separated.end_count[idx])
total_count = end_count - start_count

i = start_count
while i <= end_count:
    e_x_list = []
    e_y_list = []
    x_position_list = []
    y_position_list = []

    e_x_idx = df_data[1]['Exx'][df_data[1]['File_Number'] == i].index.tolist()
    e_y_idx = df_data[1]['Eyy'][df_data[1]['File_Number'] == i].index.tolist()
    x_position_idx = df_data[1]['X'][df_data[1]['File_Number'] == i].index.tolist()
    y_position_idx = df_data[1]['Y'][df_data[1]['File_Number'] == i].index.tolist()

    for index in e_x_idx:
        e_x_list.append(df_data[1]['Exx'].iloc[index])
        e_y_list.append(df_data[1]['Eyy'].iloc[index])
        x_position_list.append(df_data[1]['X'].iloc[index])
        y_position_list.append(df_data[1]['Y'].iloc[index])

    e_x_list = np.array(e_x_list)
    e_y_list = np.array(e_y_list)
    x_position_list = np.array(x_position_list)
    y_position_list = np.array(y_position_list)

    ### Define u and v according to x-stress and y-stress ###
    x_stress = E/(1-nu**2)*(e_x_list+nu*e_y_list-2*nu**2*e_x_list)
    y_stress = E/(1-nu**2)*(e_y_list-nu*e_x_list)
    u = x_stress
    v = y_stress
    x = x_position_list
    y = y_position_list

    fig = plt.figure(figsize=(12,8))
    fig.set_tight_layout(True)

    cycle = cycle_number_list[0]
    load = np.round(df_data[0]['load'][df_data[0]['count'] == i].iloc[0],3)

    ### Define grid and plot ###
    # x,y = np.meshgrid(np.linspace(-80,80,total_count),np.linspace(-110,110,total_count))
    plt.quiver(x,y,u,v)
    fig.suptitle(f"Stress field of {specimen} at cycle number {cycle} and a load of {load} [kN]")
    # plt.scatter(x_position_list,y_position_list)
    #plt.show()
    filename = f'Stress_field/{specimen}/{cycle}_{load}.jpg'
    plt.savefig(filename)
    print(f'Done with {filename}')
    i += 2

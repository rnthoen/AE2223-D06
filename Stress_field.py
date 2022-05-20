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
### Select which specimen you want ###
select_specimen = files[0]

if select_specimen == files[0]:
    specimen = "L103"
elif select_specimen == files[1]:
    specimen = "L104"
elif select_specimen == files[2]:
    specimen = "L105"
elif select_specimen == files[3]:
    specimen = "L109"
else: specimen = "L123"

### Select which cycle number you want to see ###
cycle_number_list = [500]

### Imports MTS data and DIC data and sequences ###
df_data = import_data(select_specimen)
df_separated = separate_sequences(df_data[0])

### Define variables ###
nu = 0.33 #Poisson ratio
E = 1 #Young's Modulus

### Find start and end in df_separated for cycle_number ###
idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number_list[0]].index.tolist()
start_count = int(df_separated.start_count[idx])
if start_count%2 != 0:
    start_count += 1
end_count = int(df_separated.end_count[idx])
total_count = end_count - start_count

i = start_count
# while i <= end_count:
### Indent everything after this to create and save stress fields for all loads in one cycle ###
e_x_list = []
e_y_list = []
x_position_list = []
y_position_list = []
e_x_start_list = []
e_y_start_list = []

e_x_idx = df_data[1]['Exx'][df_data[1]['File_Number'] == i].index.tolist()
e_y_idx = df_data[1]['Eyy'][df_data[1]['File_Number'] == i].index.tolist()
x_position_idx = df_data[1]['X'][df_data[1]['File_Number'] == i].index.tolist()
y_position_idx = df_data[1]['Y'][df_data[1]['File_Number'] == i].index.tolist()
e_x_start_idx = df_data[1]['Exx'][df_data[1]['File_Number'] == start_count].index.tolist()
e_y_start_idx = df_data[1]['Eyy'][df_data[1]['File_Number'] == start_count].index.tolist()

for index in e_x_idx:
    e_x_list.append(df_data[1]['Exx'].iloc[index])
    e_y_list.append(df_data[1]['Eyy'].iloc[index])
    x_position_list.append(df_data[1]['X'].iloc[index])
    y_position_list.append(df_data[1]['Y'].iloc[index])

for index in e_x_start_idx:
    e_x_start_list.append(df_data[1]['Exx'].iloc[index])
    e_y_start_list.append(df_data[1]['Eyy'].iloc[index])

e_x_list = np.array(e_x_list)
e_y_list = np.array(e_y_list)
x_position_list = np.array(x_position_list)
y_position_list = np.array(y_position_list)
e_x_start_list = np.array(e_x_start_list)
e_y_start_list = np.array(e_y_start_list)

### Trial with actual poisson ratio ###
### Gave really weird stress fields, which changed direction almost randomly for different loads ###
poisson = np.average(-1*(e_x_start_list/e_y_start_list))
print(poisson)

### Define u and v according to x-stress and y-stress ###
### Change 'nu' to 'poisson' when wanting to use a non-constant poisson ratio ###
# x_stress = (E/(1-nu**2))*(e_x_list+nu*e_y_list-2*nu**2*e_x_list)
# y_stress = (E/(1-nu**2))*(e_y_list-nu*e_x_list)

### Revised stress calculation which might also be correct ###
x_stress = (E/(1-poisson**2))*(e_x_list + poisson*e_y_list)
y_stress = (E/(1-poisson**2))*(e_y_list + poisson*e_x_list)

u = x_stress
v = y_stress
x = x_position_list
y = y_position_list

fig = plt.figure(figsize=(12,8))
fig.set_tight_layout(True)

cycle = cycle_number_list[0]
load = np.round(df_data[0]['load'][df_data[0]['count'] == i].iloc[0],3)

### Plot with outliers around clamp included ###
# plt.quiver(x,y,u,v)
# fig.suptitle(f"Stress field of {specimen} at cycle number {cycle} and a load of {load} [kN]")
# filename = f'Stress_field/{specimen}/{cycle}_{load}.jpg'
# # plt.savefig(filename) #Uncomment for saving file at filename location
# plt.show()
# print(f'Done with {filename}')

### Plot with outliers around clamp excluded ###
CSV_dataframe = pd.DataFrame({"x":x,"y":y,"u":u,"v":v})
# Order of exclusions:
# Left-top clamp - Right-top clamp - Left-bottom clamp - Right-bottom clamp
if specimen == 'L103':
    CSV_dataframe[(CSV_dataframe['x'] >= -85) & (CSV_dataframe['x'] <= -56) & (CSV_dataframe['y'] >= 90) & (CSV_dataframe['y'] <= 120)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 54) & (CSV_dataframe['x'] <= 70) & (CSV_dataframe['y'] >= 60) & (CSV_dataframe['y'] <= 90)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= -80) & (CSV_dataframe['x'] <= -45) & (CSV_dataframe['y'] >= -77) & (CSV_dataframe['y'] <= -50)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 56) & (CSV_dataframe['x'] <= 80) & (CSV_dataframe['y'] >= -115) & (CSV_dataframe['y'] <= -80)] = 0
elif specimen == 'L104':
    CSV_dataframe[(CSV_dataframe['x'] >= -80) & (CSV_dataframe['x'] <= -55) & (CSV_dataframe['y'] >= 90) & (CSV_dataframe['y'] <= 120)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 52) & (CSV_dataframe['x'] <= 72) & (CSV_dataframe['y'] >= 65) & (CSV_dataframe['y'] <= 85)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= -80) & (CSV_dataframe['x'] <= -53) & (CSV_dataframe['y'] >= -78) & (CSV_dataframe['y'] <= -52)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 54) & (CSV_dataframe['x'] <= 74) & (CSV_dataframe['y'] >= -115) & (CSV_dataframe['y'] <= -85)] = 0
elif specimen == 'L105':
    CSV_dataframe[(CSV_dataframe['x'] >= -75) & (CSV_dataframe['x'] <= -50) & (CSV_dataframe['y'] >= 85) & (CSV_dataframe['y'] <= 120)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 56) & (CSV_dataframe['x'] <= 71) & (CSV_dataframe['y'] >= 60) & (CSV_dataframe['y'] <= 85)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= -80) & (CSV_dataframe['x'] <= -53) & (CSV_dataframe['y'] >= -82) & (CSV_dataframe['y'] <= -50)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 52) & (CSV_dataframe['x'] <= 75) & (CSV_dataframe['y'] >= -115) & (CSV_dataframe['y'] <= -85)] = 0
elif specimen == 'L109':
    CSV_dataframe[(CSV_dataframe['x'] >= -85) & (CSV_dataframe['x'] <= -55) & (CSV_dataframe['y'] >= 83) & (CSV_dataframe['y'] <= 118)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 56) & (CSV_dataframe['x'] <= 75) & (CSV_dataframe['y'] >= 56) & (CSV_dataframe['y'] <= 85)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= -80) & (CSV_dataframe['x'] <= -54) & (CSV_dataframe['y'] >= -84) & (CSV_dataframe['y'] <= -57)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 53) & (CSV_dataframe['x'] <= 75) & (CSV_dataframe['y'] >= -115) & (CSV_dataframe['y'] <= -85)] = 0
elif specimen == 'L123':
    CSV_dataframe[(CSV_dataframe['x'] >= -85) & (CSV_dataframe['x'] <= -54) & (CSV_dataframe['y'] >= 90) & (CSV_dataframe['y'] <= 120)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 56) & (CSV_dataframe['x'] <= 75) & (CSV_dataframe['y'] >= 62) & (CSV_dataframe['y'] <= 80)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= -80) & (CSV_dataframe['x'] <= -49) & (CSV_dataframe['y'] >= -79) & (CSV_dataframe['y'] <= -50)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= 52) & (CSV_dataframe['x'] <= 75) & (CSV_dataframe['y'] >= -110) & (CSV_dataframe['y'] <= -81)] = 0
    CSV_dataframe[(CSV_dataframe['x'] >= -81) & (CSV_dataframe['x'] <= -77) & (CSV_dataframe['y'] <= 90) & (CSV_dataframe['y'] >= -81)] = 0

#CSV_dataframe.to_csv(f'Stress_field/CSV_files/{specimen}_{cycle}_{load}.csv')

plt.quiver(CSV_dataframe['x'],CSV_dataframe['y'],CSV_dataframe['u'],CSV_dataframe['v'])
fig.suptitle(f"Stress field of {specimen} at cycle number {cycle} and a load of {load} [kN]")
filename = f'Stress_field/{specimen}/{cycle}_{load}.jpg'
#plt.savefig(filename) #Uncomment for saving file at filename location
#plt.show()
# print(f'Exx equals {e_x_list[345]}')
# print(f'Eyy equals {e_y_list[345]}')
# print(f'At ({CSV_dataframe["x"].iloc[345]},{CSV_dataframe["y"].iloc[345]}), v equals {CSV_dataframe["v"].iloc[345]}')
print(f'Done with {filename}')

# i += 2 #Uncomment when using while loop

import numpy as np

from import_data import import_data
from separate_sequences import separate_sequences
from poisson import poisson
from poisson import poisson_avg
from heatmap_data import heatmap_data
from heatmap_plot import heatmap_plot
from stiffness_coefficient import stiffness

files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840.csv', 'Data/L103/L1-03_8842_2_13994.csv', 'Data/L103/L1-03_13996_2_16696.csv'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160.csv', 'Data/L104/L1-04_4162_2_8548.csv', 'Data/L104/L1-04_8550_2_12242.csv', 'Data/L104/L1-04_12244_2_16402.csv', 'Data/L104/L1-04_16404_2_20098.csv', 'Data/L104/L1-04_20100_2_23800.csv', 'Data/L104/L1-04_23802_2_27262.csv', 'Data/L104/L1-04_27264_2_30036.csv', 'Data/L104/L1-04_30038_2_31422.csv'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050.csv', 'Data/L105/L1-05_4052_2_7978.csv', 'Data/L105/L1-05_7980_2_12136.csv', 'Data/L105/L1-05_12138_2_15722.csv'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016.csv', 'Data/L109/L1-09_4018_2_8288.csv', 'Data/L109/L1-09_8290_2_12072.csv', 'Data/L109/L1-09_12074_2_14760.csv'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000.csv', 'Data/L123/L1-23_4002_2_8080.csv', 'Data/L123/L1-23_8082_2_12430.csv', 'Data/L123/L1-23_12432_2_15850.csv', 'Data/L123/L1-23_15852_2_20506.csv', 'Data/L123/L1-23_20508_2_24236.csv', 'Data/L123/L1-23_24238_2_28894.csv', 'Data/L123/L1-23_28896_2_31384.csv', 'Data/L123/L1-23_31386_2_35416.csv', 'Data/L123/L1-23_35418_2_40390.csv', 'Data/L123/L1-23_40392_2_42256.csv']]

select_specimen = files[0]

df_data = import_data(select_specimen)
df_separated = separate_sequences(df_data[0])
df_separated.to_csv(f'separated_sequences_{select_specimen[0][5:9]}.csv')

#Make  stiffness coeficient plots
#buckle = np.ones(len(df_separated[0]))*(-20)
buckle = np.linspace(-25, -15, len(df_separated))
k1, k2 = stiffness(buckle, df_separated, df_data[0])


# poisson heat maps
path = "L103"                           # select folder to put figures in

mid_cycle = round(len(df_separated.cycle_number) / 2)
end_cycle = len(df_separated.cycle_number)-1
cycle_numbers = [df_separated.cycle_number[0], df_separated.cycle_number[mid_cycle], df_separated.cycle_number[end_cycle]]

start_counts = []
end_counts = []

for cycle_number in cycle_numbers:
    start_count = df_separated["start_count"].loc[df_separated["cycle_number"] == cycle_number].iloc[0]
    end_count = df_separated["end_count"].loc[df_separated["cycle_number"] == cycle_number].iloc[0]
    # obtain even number count
    if start_count % 2 != 0:
        start_count += 1
    if end_count % 2 != 0:
        end_count -= 1
    start_counts.append(start_count)        # obtain starting count for given cycle number
    end_counts.append(end_count)            # obtain ending count for given cycle number

while 0 != min(np.array(end_counts) - np.array(start_counts)):
    # loop from start count to end count to obtain heat maps at each count number
    poisson(df_data, start_counts, select_specimen[0][5:9], cycle_numbers, path)
    start_counts = start_counts + np.array([2, 2, 2])       # increment count number

# Calculate average poisson values for skin and stiffener
count = 8122              # Count value at which to take the average -- L103: 8122    L104: 42    L105: 7698   L123: 40
x_bounds = [[-70, -40],   # upper and lower bound x-value for skin/stiffener
            [-20, 20]]
y_bounds = [[-10, 10],    # upper and lower bound y-value for skin/stiffener
            [50, 60]]
print(poisson_avg(df_data, count, x_bounds, y_bounds))  # returns 2 poisson averages, for skin and stiffener area


# Make heatmap plot
cycle_number = 500
count_offset = 6
variable = 'Exy'
plot_data = heatmap_data(cycle_number, count_offset, df_separated, df_data[1], variable)

point_size = 40
colormap = 'coolwarm'
color_label = 'Exy [-]'
count = plot_data[4]
plot_title = f'{select_specimen[0][5:9]}, {cycle_number} cycles, count = {count}'
filename = f'Heatmap/{select_specimen[0][5:9]}_{cycle_number}_{count}.jpg'
heatmap_plot(plot_data, point_size, colormap, color_label, plot_title, filename, (-0.005, 0.005))

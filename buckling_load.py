'''
Determine buckling load
'''

from import_data import import_data
from separate_sequences import separate_sequences
from lookup_DIC_data import lookup_DIC_data
from interpolate_panel import interpolate_panel

import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


# Convert specimen string to index
def specimen_to_idx(specimen):
    if specimen == 'L103':
        return 0
    elif specimen == 'L104':
        return 1
    elif specimen == 'L105':
        return 2
    elif specimen == 'L109':
        return 3
    elif specimen == 'L123':
        return 4

# Setup figure
fig = plt.figure(figsize=(12, 8))
fig.set_tight_layout(True)

# Determine buckling load
def determine_buckling_load(files, specimen, cycle_number, parameter, unit, threshold, points, df_data, df_separated):

    # print(cycle_number)

    # Find start and end of cycle
    #print('Finding start and end')
    idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number].index.tolist()
    start_count = int(df_separated.start_count[idx])
    end_count = int(df_separated.end_count[idx])

    # Loop through all counts in cycle
    ax = plt.subplot()
    buckling_forces = [[], []]

    for point in points:
        #print(f'Creating force-parameter list for ({round(point[0], 1)}, {round(point[1], 1)})')
        # Create force-parameter lists
        DIC_data = lookup_DIC_data(cycle_number, df_separated, df_data, point[0], point[1], parameter)

        force_list = DIC_data[1]
        parameter_list = DIC_data[2]

        #print(f'Calculating deltas for ({round(point[0], 1)}, {round(point[1], 1)})')
        # Create parameter deltas list
        deltas_list = []
        for i in range(1, len(force_list)):
            parameter_delta = parameter_list[i] - parameter_list[i - 1]
            absolute_parameter_delta = abs(parameter_delta)
            deltas_list.append(absolute_parameter_delta)
        force_list.pop(0)

        # Interpolate deltas
        interpolation_steps = 3000
        interpolated_force_list = np.linspace(max(force_list), min(force_list), interpolation_steps)
        interpolate_function = interpolate.interp1d(force_list, deltas_list)
        interpolated_deltas_list = interpolate_function(interpolated_force_list)

        # # ======================================================================
        # # TODO: Make this based on acceleration
        #
        # second_deltas_list = []
        # for i in range(1, len(force_list)):
        #
        #     # print(interpolated_deltas_list[i], interpolated_deltas_list[i - 1], interpolated_deltas_list[i] - interpolated_deltas_list[i - 1])
        #     parameter_second_delta = deltas_list[i] - deltas_list[i - 1]
        #     absolute_parameter_second_delta = abs(parameter_second_delta)
        #     second_deltas_list.append(absolute_parameter_second_delta)
        #
        # # ax.plot(interpolated_force_list, interpolated_deltas_list, label = 'delta')
        # # ax.plot(force_list[1:], second_deltas_list, label = f'{point}', alpha = 0.5)
        #
        # # Find the index of the maximum value in the second_deltas_list
        # buckling_idx = second_deltas_list.index(max(second_deltas_list))
        #
        # # ======================================================================


        # print(f'Detecting threshold intersection for ({round(point[0], 1)}, {round(point[1], 1)})')

        # Detect threshold intersection
        for i in range(len(interpolated_deltas_list)):
            if interpolated_deltas_list[i] >= threshold:
                if interpolated_force_list[i] > -30:
                    buckling_forces[0].append(interpolated_force_list[i])
                    buckling_forces[1].append(interpolated_deltas_list[i])
                else:
                    print(f'30 kN thingy happened for i = {i}')
                break

        # Plot deltas
        ax.plot(interpolated_force_list, interpolated_deltas_list, zorder = 2, alpha = 1, label = f'({round(point[0], 1)}, {round(point[1], 1)})')

    # Determine buckling force
    buckling_force = np.mean(buckling_forces[0])
    stdev = np.std(buckling_forces[0])
    #print(f'F_buckle = {round(buckling_force, 1)} ± {round(2 * stdev, 1)} [kN]')

    # Plot things
    ax.scatter(buckling_forces[0], buckling_forces[1], label = f'Buckling Point', color = 'black', zorder = 3)
    ax.hlines(threshold, -100, 100, color = 'red', linewidth = 2, linestyle = 'dashed', label = f'Threshold = {threshold} [mm]', zorder = 3, alpha = 0.5)
    ax.scatter(buckling_forces[0], buckling_forces[1], label = f'Threshold intersection', color = 'red', zorder = 4)
    ax.vlines(buckling_force, -100, 100, linestyle = 'dashed', zorder = 3, linewidth = 2, color = 'blue', label = f'F_buckle = {round(buckling_force, 1)} [kN]')
    ax.fill_betweenx((-100, 100), buckling_force - 2 * stdev, buckling_force - 1 * stdev, color = 'green', zorder = 1, alpha = 0.3, label = f'95% interval = ± {round(2 * stdev, 1)} [kN]')
    ax.fill_betweenx((-100, 100), buckling_force + 1 * stdev, buckling_force + 2 * stdev, color = 'green', zorder = 1, alpha = 0.3)
    ax.fill_betweenx((-100, 100), buckling_force - 1 * stdev, buckling_force + 1 * stdev, color = 'blue', zorder = 0, alpha = 0.3, label = f'68% interval = ± {round(1 * stdev, 1)} [kN]')


    # Setup figure
    ax.invert_xaxis()
    ax.set_xlabel(f'F [kN]')
    ax.set_ylabel(f'Δ{parameter} [{unit}]')
    ax.set_xlim(left = max(force_list) + 7, right = min(force_list) - 5)
    ax.set_ylim(bottom = min(deltas_list) - 0.1, top = max(deltas_list) + 0.1)

    plt.title(f'{select_specimen[0][5:9]} at {cycle_number} cycles')
    plt.legend(loc="upper right")
    plt.savefig(f'BucklingLoad/Detection/BucklingDetection_{select_specimen[0][5:9]}_{cycle_number}.svg')
    ax.clear()

    result = [cycle_number, buckling_force, stdev]

    return result

# Look-up table for filenames
files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840.csv', 'Data/L103/L1-03_8842_2_13994.csv', 'Data/L103/L1-03_13996_2_16696.csv'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160.csv', 'Data/L104/L1-04_4162_2_8548.csv', 'Data/L104/L1-04_8550_2_12242.csv', 'Data/L104/L1-04_12244_2_16402.csv', 'Data/L104/L1-04_16404_2_20098.csv', 'Data/L104/L1-04_20100_2_23800.csv', 'Data/L104/L1-04_23802_2_27262.csv', 'Data/L104/L1-04_27264_2_30036.csv', 'Data/L104/L1-04_30038_2_31422.csv'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050.csv', 'Data/L105/L1-05_4052_2_7978.csv', 'Data/L105/L1-05_7980_2_12136.csv', 'Data/L105/L1-05_12138_2_15722.csv'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016.csv', 'Data/L109/L1-09_4018_2_8288.csv', 'Data/L109/L1-09_8290_2_12072.csv', 'Data/L109/L1-09_12074_2_14760.csv'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000.csv', 'Data/L123/L1-23_4002_2_8080.csv', 'Data/L123/L1-23_8082_2_12430.csv', 'Data/L123/L1-23_12432_2_15850.csv', 'Data/L123/L1-23_15852_2_20506.csv', 'Data/L123/L1-23_20508_2_24236.csv', 'Data/L123/L1-23_24238_2_28894.csv', 'Data/L123/L1-23_28896_2_31384.csv', 'Data/L123/L1-23_31386_2_35416.csv', 'Data/L123/L1-23_35418_2_40390.csv', 'Data/L123/L1-23_40392_2_42256.csv']]

# Input specimen, cycles and parameter
specimen = 'L104'
parameter = 'W'
unit = 'mm'
threshold = 0.1

# Input points to evaluate
N_points = 8
# x_points = list(np.linspace(-70, 70, N_points))
# y_points = list(np.linspace(0, 0, N_points))
x_points = [-70, -50, -30, 30, 50, 70]
y_points = [0, 0, 0, 0, 0, 0]
points = [[x_points[i], y_points[i]] for i in range(0, len(x_points))]

# Generate look-up tables
select_specimen = files[specimen_to_idx(specimen)]
#print('Importing data')
df_data = import_data(select_specimen)
#print('Separating sequences')
df_separated = separate_sequences(df_data[0])
df_separated.to_csv(f'separated_sequences_{select_specimen[0][5:9]}.csv')

# Good old massive loop
buckling_loads = []
low_limit_1 = []
upp_limit_1 = []
low_limit_2 = []
upp_limit_2 = []
stdevs = []
# cycle_numbers = [500, 5500, 10500, 15500, 20500]
cycle_numbers = df_separated.cycle_number

for cycle_number in cycle_numbers:
    buckling_result = determine_buckling_load(files, specimen, cycle_number, parameter, unit, threshold, points, df_data, df_separated)
    print(buckling_result)
    buckling_loads.append(buckling_result[1])
    stdevs.append(buckling_result[2])
    low_limit_1.append(buckling_result[1] + buckling_result[2])
    upp_limit_1.append(buckling_result[1] - buckling_result[2])
    low_limit_2.append(buckling_result[1] + 2 * buckling_result[2])
    upp_limit_2.append(buckling_result[1] - 2 * buckling_result[2])

# Save results
df = pd.DataFrame({'cycle_number': cycle_numbers, 'buckling_load': buckling_loads, 'stdev': stdevs})
df.to_csv(f'BucklingLoad/buckling_load_{specimen}_{parameter}_{threshold}.csv')

# Plot results
ax = plt.subplot()
ax.fill_between(cycle_numbers, low_limit_2, upp_limit_2, color = 'green', zorder = 1, alpha = 0.3, label = f'95% interval')
ax.fill_between(cycle_numbers, low_limit_1, upp_limit_1, color = 'blue', zorder = 0, alpha = 0.3, label = f'68% interval')
ax.plot(cycle_numbers, buckling_loads, label = 'F_buckle')
ax.invert_yaxis()

plt.title(f'F_buckle of {specimen}')
plt.xlabel('Cycles [-]')
plt.ylabel('F_buckle [kN]')
plt.legend()
plt.savefig(f'buckling_load_{specimen}.svg')
plt.show()

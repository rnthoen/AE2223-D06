"""
Determine bucking load with only MTS dataset
Create a folder called 'MTS_buckling' for the images
"""

# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

# Import functions
from import_data import import_data
from separate_sequences import separate_sequences
from axial_curve_data import axial_curve_data

# Do you want to make some plots?
make_plots = True

# Do you want to show the plots?
show_plots = False

# Do you want to get (very) detailed progress printouts?
do_print = False

# Create results lists
buckling_loads = []
stdevs = []

# Specify location of dataset
files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840.csv', 'Data/L103/L1-03_8842_2_13994.csv', 'Data/L103/L1-03_13996_2_16696.csv'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160.csv', 'Data/L104/L1-04_4162_2_8548.csv', 'Data/L104/L1-04_8550_2_12242.csv', 'Data/L104/L1-04_12244_2_16402.csv', 'Data/L104/L1-04_16404_2_20098.csv', 'Data/L104/L1-04_20100_2_23800.csv', 'Data/L104/L1-04_23802_2_27262.csv', 'Data/L104/L1-04_27264_2_30036.csv', 'Data/L104/L1-04_30038_2_31422.csv'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050.csv', 'Data/L105/L1-05_4052_2_7978.csv', 'Data/L105/L1-05_7980_2_12136.csv', 'Data/L105/L1-05_12138_2_15722.csv'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016.csv', 'Data/L109/L1-09_4018_2_8288.csv', 'Data/L109/L1-09_8290_2_12072.csv', 'Data/L109/L1-09_12074_2_14760.csv'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000.csv', 'Data/L123/L1-23_4002_2_8080.csv', 'Data/L123/L1-23_8082_2_12430.csv', 'Data/L123/L1-23_12432_2_15850.csv', 'Data/L123/L1-23_15852_2_20506.csv', 'Data/L123/L1-23_20508_2_24236.csv', 'Data/L123/L1-23_24238_2_28894.csv', 'Data/L123/L1-23_28896_2_31384.csv', 'Data/L123/L1-23_31386_2_35416.csv', 'Data/L123/L1-23_35418_2_40390.csv', 'Data/L123/L1-23_40392_2_42256.csv']]

# Select specimen
select_specimen = files[4]
specimen = select_specimen[0][5:9]

# Generate lookup tables
if do_print:
    print(f'Importing data for {specimen}')
df_data = import_data(select_specimen)
if do_print:
    print('Separating sequences')
df_separated = separate_sequences(df_data[0])

# Select sequence
# cycle_number_list = [3000]
cycle_number_list = df_separated.cycle_number.to_list()

# Loop through all cycles
for cycle_number in cycle_number_list:
    # Get MTS data
    if do_print:
        print(f'Looking up sequences at {cycle_number} cycles')
    MTS_data = axial_curve_data([cycle_number], df_separated, df_data[0])
    x = np.array(MTS_data[0][2])
    y = np.array(MTS_data[0][1])

    # Create first model line
    if do_print:
        print('Creating first model')
    E = 85                                                      # We guess that E = 85 kN/mm
    x_model = x
    y_model = x * E - y[0]

    # Plot MTS data
    if make_plots:
        fig = plt.figure(figsize=(10, 10))
        fig.set_tight_layout(True)
        ax = plt.subplot(3, 2, 1)
        ax.plot(x, y, label = 'MTS data', color = 'black')
        ax.plot(x_model, y_model, label = f'Initial model (E = {E} kN/mm)', color = 'black', linestyle = 'dashed')
        ax.set_xlabel('d [mm]')
        ax.set_ylabel('F [kN]')
        ax.invert_xaxis()
        ax.invert_yaxis()
        ax.set_title('Step #1: Plot the MTS data and guess the linear slope')
        plt.legend()

    # Calculate delta between model and data
    if do_print:
        print('Calculating deltas for first model')
    y_delta_model = abs(y_model - y)

    # Determine buckling point based on first model
    if do_print:
        print('Determining buckling point for first model')
                                               # We set a margin of 1 kN here
    avg_range = 3                                               #  We take the initial delta as the average of the first 3 data points
    y_start = np.ones(len(x)) * np.average(y_delta_model[0:avg_range])
    # y_threshold = y_start * threshold
    y_threshold = y_start + 1
    i = avg_range + 1
    while (y_delta_model[i] < y_threshold[i]):
        i += 1
    x_buckling = x[i]
    y_buckling = y[i]
    y_delta_buckling = y_delta_model[i]

    # Plot initial model estimation
    if make_plots:
        ax2 = plt.subplot(3, 2, 2)
        ax2.plot(x, y_delta_model, label = 'Delta between Initial model and MTS data', color = 'black')
        ax2.plot(x, y_threshold, label = 'Threshold delta', color = 'black', linestyle = 'dashed')
        ax2.scatter(x_buckling, y_delta_buckling, label = f'Estimated buckling (at {round(y_buckling, 2)} kN)', color = 'red')
        ax2.set_xlabel('d [mm]')
        ax2.set_ylabel('ΔF [kN]')
        ax2.invert_xaxis()
        ax2.set_title('Step #2: Look where the delta begins to deviate')
        plt.legend()

    # Select data range for least-squares approximation
    if do_print:
        print('Selecting data for least-squares approximation')
    x_select = x[0:i]
    y_select = y[0:i]

    # Approximate linear part with least-squares
    if do_print:
        print('Finding least-squares solution')
    A = np.vstack([x_select, np.ones(i)]).transpose()
    m, c = np.linalg.lstsq(A, y_select, rcond=None)[0]

    # Make line of least-squares solution
    x_lstsq = x
    y_lstsq = x * m + c

    # Plot least-squares approximation
    if make_plots:
        ax3 = plt.subplot(3, 2, 3)
        ax3.plot(x, y, label = 'MTS data', color = 'black')
        ax3.plot(x_lstsq, y_lstsq, label = 'Fitted model', color = 'black', linestyle = 'dashed')
        ax3.set_xlabel('d [mm]')
        ax3.set_ylabel('F [kN]')
        ax3.invert_xaxis()
        ax3.invert_yaxis()
        ax3.set_title('Step #3: Update model with least-squares estimation')
        plt.legend()

    # Calculate delta between least-squares solution and data
    if do_print:
        print('Calculating deltas for least-squares approximation')
    y_delta_lstsq = abs(y_lstsq - y)

    # Determine buckling point based on least-squares approximation
    if do_print:
        print('Determining buckling point for least-squares approximation')
    y_start = np.ones(len(x)) * np.average(y_delta_lstsq[0:i])
    # y_threshold = y_start * threshold
    y_threshold = y_start + 0.5                                         # Here, margin of 0.5 kN

    # Interpolation
    N_interp = len(x) * 10
    interpolate_function_lstsq = interpolate.interp1d(x, y)
    interpolate_deltas_function_lstsq = interpolate.interp1d(x, y_delta_lstsq)

    x_interp_lstsq = np.linspace(max(x), min(x), N_interp)
    y_interp_lstsq = interpolate_function_lstsq(x_interp_lstsq)
    y_delta_interp_lstsq = interpolate_deltas_function_lstsq(x_interp_lstsq)

    j = i - 1
    while (y_delta_interp_lstsq[j] < y_threshold[0]):
        j += 1

    x_buckling_lstsq = x_interp_lstsq[j]
    y_buckling_lstsq = y_interp_lstsq[j]
    y_delta_buckling_lstsq = y_delta_interp_lstsq[j]
    buckling_force = y_buckling_lstsq

    # Plot least-squares approximation
    if make_plots:
        ax4 = plt.subplot(3, 2, 4)
        # ax4.plot(x, y_delta_lstsq, label = 'Delta between Fitted model and MTS data', color = 'black')
        ax4.plot(x_interp_lstsq, y_delta_interp_lstsq, label = 'Interpolated delta between Fitted model and MTS data', color = 'black')
        ax4.plot(x, y_threshold, label = 'Threshold delta', color = 'black', linestyle = 'dashed')
        ax4.scatter(x_buckling_lstsq, y_delta_buckling_lstsq, label = f'Estimated buckling (at {round(buckling_force, 2)} kN)', color = 'red')
        ax4.set_xlabel('d [mm]')
        ax4.set_ylabel('ΔF [kN]')
        ax4.invert_xaxis()
        ax4.set_title('Step #4: Again, look where the delta begins to deviate')
        plt.legend()

    # Plot solution
    if make_plots:
        ax5 = plt.subplot(3, 2, 5)
        ax5.plot(x, y, label = 'MTS data', color = 'black')
        ax5.plot(x_lstsq, y_lstsq, label = 'Fitted model', color = 'black', linestyle = 'dashed')
        ax5.scatter(x_buckling_lstsq, y_buckling_lstsq, label = f'Estimated buckling (at {round(buckling_force, 2)} kN)', color = 'red')
        ax5.set_xlabel('d [mm]')
        ax5.set_ylabel('F [kN]')
        ax5.invert_xaxis()
        ax5.invert_yaxis()
        ax5.set_title('Step #5: Look up buckling force')
        plt.legend()

    if make_plots:
        plt.savefig(f'MTS_buckling/{specimen}/{specimen}_{cycle_number}_MTS_buckling.png')
        if show_plots:
            plt.show()

    buckling_loads.append(buckling_force)
    stdevs.append(2)    # TODO: Different margin
    print(f'\rCycle {cycle_number}/{cycle_number_list[-1]} ({int(100 * cycle_number / cycle_number_list[-1])}%)', end='')

# Save results
df = pd.DataFrame({'cycle_number': cycle_number_list, 'buckling_load': buckling_loads, 'stdev': stdevs})
df.to_csv(f'MTS_buckling/{specimen}_MTS_buckling.csv')

print(f'\nDone!')

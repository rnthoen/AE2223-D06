import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits import mplot3d

from import_data import import_data
from separate_sequences import separate_sequences
from axial_curve_data import axial_curve_data
from min_max_displacement import min_max_displacement
from poisson import poisson
from heatmap_data import heatmap_data
from heatmap_plot import heatmap_plot
from interpolate_panel import interpolate_panel

files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840.csv', 'Data/L103/L1-03_8842_2_13994.csv', 'Data/L103/L1-03_13996_2_16696.csv'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160.csv', 'Data/L104/L1-04_4162_2_8548.csv', 'Data/L104/L1-04_8550_2_12242.csv', 'Data/L104/L1-04_12244_2_16402.csv', 'Data/L104/L1-04_16404_2_20098.csv', 'Data/L104/L1-04_20100_2_23800.csv', 'Data/L104/L1-04_23802_2_27262.csv', 'Data/L104/L1-04_27264_2_30036.csv', 'Data/L104/L1-04_30038_2_31422.csv'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050.csv', 'Data/L105/L1-05_4052_2_7978.csv', 'Data/L105/L1-05_7980_2_12136.csv', 'Data/L105/L1-05_12138_2_15722.csv'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016.csv', 'Data/L109/L1-09_4018_2_8288.csv', 'Data/L109/L1-09_8290_2_12072.csv', 'Data/L109/L1-09_12074_2_14760.csv'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000.csv', 'Data/L123/L1-23_4002_2_8080.csv', 'Data/L123/L1-23_8082_2_12430.csv', 'Data/L123/L1-23_12432_2_15850.csv', 'Data/L123/L1-23_15852_2_20506.csv', 'Data/L123/L1-23_20508_2_24236.csv', 'Data/L123/L1-23_24238_2_28894.csv', 'Data/L123/L1-23_28896_2_31384.csv', 'Data/L123/L1-23_31386_2_35416.csv', 'Data/L123/L1-23_35418_2_40390.csv', 'Data/L123/L1-23_40392_2_42256.csv']]

select_specimen = files[0]

df_data = import_data(select_specimen)
df_separated = separate_sequences(df_data[0])
df_separated.to_csv(f'separated_sequences_{select_specimen[0][5:9]}.csv')

N = 14700
while N <= 14762:

    print(N)

    DIC_df = df_data[1]
    MTS_df = df_data[0]
    grid_x, grid_y = np.mgrid[-80:80:200j, -110:110:200j]
    #N = 14700
    W_displacement = interpolate_panel(DIC_df, N, grid_x, grid_y, "W")
    load = MTS_df.loc[MTS_df['count'] == N]["load"].iloc[0]


    # Make heatmap plot
    cycle_number = 135500
    count_offset = 6
    variable = 'Z'
    plot_data = np.vstack((grid_x.flatten(), grid_y.flatten(), W_displacement.flatten()))
    #plot_data = heatmap_data(cycle_number, count_offset, df_separated, df_data[1], variable)

    point_size = 40
    colormap = 'rainbow'
    color_label = 'Z [mm]'
    count = N
    plot_title = f'{select_specimen[0][5:9]}, {cycle_number} cycles, count = {count}'
    filename = f'Heatmap/{variable}/{select_specimen[0][5:9]}_{cycle_number}_{count}.jpg'
    heatmap_plot(plot_data, point_size, colormap, color_label, plot_title, filename, (-0.005, 0.005))

    N += 2

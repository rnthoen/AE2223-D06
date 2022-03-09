import pandas as pd
import matplotlib.pyplot as plt

from import_data import import_data
from separate_sequences import separate_sequences
from axial_curve_data import axial_curve_data
from min_max_displacement import min_max_displacement

files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840.csv', 'Data/L103/L1-03_8842_2_13994.csv', 'Data/L103/L1-03_13996_2_16696.csv'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160.csv', 'Data/L104/L1-04_4162_2_8548.csv', 'Data/L104/L1-04_8550_2_12242.csv', 'Data/L104/L1-04_12244_2_16402.csv', 'Data/L104/L1-04_16404_2_20098.csv', 'Data/L104/L1-04_20100_2_23800.csv', 'Data/L104/L1-04_23802_2_27262.csv', 'Data/L104/L1-04_27264_2_30036.csv', 'Data/L104/L1-04_30038_2_31422.csv'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050.csv', 'Data/L105/L1-05_4052_2_7978.csv', 'Data/L105/L1-05_7980_2_12136.csv', 'Data/L105/L1-05_12138_2_15722.csv'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016.csv', 'Data/L109/L1-09_4018_2_8288.csv', 'Data/L109/L1-09_8290_2_12072.csv', 'Data/L109/L1-09_12074_2_14760.csv'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000.csv', 'Data/L123/L1-23_4002_2_8080.csv', 'Data/L123/L1-23_8082_2_12430.csv', 'Data/L123/L1-23_12432_2_15850.csv', 'Data/L123/L1-23_15852_2_20506.csv', 'Data/L123/L1-23_20508_2_24236.csv', 'Data/L123/L1-23_24238_2_28894.csv', 'Data/L123/L1-23_28896_2_31384.csv', 'Data/L123/L1-23_31386_2_35416.csv', 'Data/L123/L1-23_35418_2_40390.csv', 'Data/L123/L1-23_40392_2_42256.csv']]

select_specimen = files[0]

df_data = import_data(select_specimen)

df_separated = separate_sequences(df_data[0])
df_separated.to_csv(f'separated_sequences_{select_specimen[0][5:9]}.csv')

# Make axial curve plot
cycle_number_list = [500]
plot_data = axial_curve_data(cycle_number_list, df_separated, df_data[0])

# plt.scatter(plot_data[0][2], plot_data[0][1])
# plt.xlabel('Displacement [mm]')
# plt.ylabel('Load [kN]')
# plt.show()

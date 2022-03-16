import pandas as pd
import matplotlib.pyplot as plt

from separate_sequences import separate_sequences
from import_data import import_data

# cycle_number_list is an array like [500, 1000, 1500]
# df_separated is the output of the separate_sequences() function
# df_data should look like "df_data[0]"

files = [['Data/L103/L1-03.csv', 'Data/L103/L1-03_0_2_4052.csv', 'Data/L103/L1-03_4054_2_8840.csv', 'Data/L103/L1-03_8842_2_13994.csv', 'Data/L103/L1-03_13996_2_16696.csv'],
         ['Data/L104/L1-04.csv', 'Data/L104/L1-04_0_2_4160.csv', 'Data/L104/L1-04_4162_2_8548.csv', 'Data/L104/L1-04_8550_2_12242.csv', 'Data/L104/L1-04_12244_2_16402.csv', 'Data/L104/L1-04_16404_2_20098.csv', 'Data/L104/L1-04_20100_2_23800.csv', 'Data/L104/L1-04_23802_2_27262.csv', 'Data/L104/L1-04_27264_2_30036.csv', 'Data/L104/L1-04_30038_2_31422.csv'],
         ['Data/L105/L1-05.csv', 'Data/L105/L1-05_0_2_4050.csv', 'Data/L105/L1-05_4052_2_7978.csv', 'Data/L105/L1-05_7980_2_12136.csv', 'Data/L105/L1-05_12138_2_15722.csv'],
         ['Data/L109/L1-09.csv', 'Data/L109/L1-09_0_2_4016.csv', 'Data/L109/L1-09_4018_2_8288.csv', 'Data/L109/L1-09_8290_2_12072.csv', 'Data/L109/L1-09_12074_2_14760.csv'],
         ['Data/L123/L1-23.csv', 'Data/L123/L1-23_0_2_4000.csv', 'Data/L123/L1-23_4002_2_8080.csv', 'Data/L123/L1-23_8082_2_12430.csv', 'Data/L123/L1-23_12432_2_15850.csv', 'Data/L123/L1-23_15852_2_20506.csv', 'Data/L123/L1-23_20508_2_24236.csv', 'Data/L123/L1-23_24238_2_28894.csv', 'Data/L123/L1-23_28896_2_31384.csv', 'Data/L123/L1-23_31386_2_35416.csv', 'Data/L123/L1-23_35418_2_40390.csv', 'Data/L123/L1-23_40392_2_42256.csv']]

select_specimen = files[0]

df_data = import_data(select_specimen)

df_separated = separate_sequences(df_data[0])

def strain_load_curve_data(cycle_number_list, df_separated, df_data):

    result = []
    for cycle_number in cycle_number_list:

        # find start and end in df_separated for cycle_number
        idx = df_separated.cycle_number[df_separated.cycle_number == cycle_number].index.tolist()
        start_count = int(df_separated.start_count[idx])
        end_count = int(df_separated.end_count[idx])

        # find load and displacement for each point from start to end (both incl.)
        load_list = []
        strain_median_list = []
        strain_min_list = []
        strain_max_list = []
        strain2_list = []

        i = start_count
        while i <= end_count:
            if i%2 == 0:
                idx = df_data[0]['count'][df_data[0]['count'] == i].index.tolist()
                load = float(df_data[0].load[idx])
                load_list.append(load)
                idx1 = df_data[1]['File_Number'][df_data[1]['File_Number'] == i].index.tolist()
                idx2 = round((idx1[0] + idx1[-1]) / len(idx1))
                Exx_strain_median = df_data[1]["Eyy"].iloc[idx2]
                strain_median_list.append(Exx_strain_median)
                for k in idx1:
                    strain2_list.append(df_data[1]["Eyy"].iloc[k])
                strain_min_list.append(min(strain2_list))
                strain_max_list.append(max(strain2_list))
                strain2_list = []
            i += 1

        # format in a return array
        result.append([cycle_number, load_list, strain_min_list, strain_median_list, strain_max_list])

    return result

cycle_number_list = [50500,100500,150500]
plot_data = strain_load_curve_data(cycle_number_list, df_separated, df_data)
#print(plot_data[0][1],plot_data[0][2])

fig, axs = plt.subplots(4,constrained_layout=True)
for j in range(len(cycle_number_list)):
    #axs[0,0] = plt.subplot(111)
    axs[0].plot(plot_data[j][1], plot_data[j][2], label = f'{cycle_number_list[j]} cycles')
    axs[0].invert_xaxis()
    axs[0].invert_yaxis()
    axs[0].set_title('Minimum strain - Load')
    axs[0].legend(bbox_to_anchor=(1.04,1), loc="upper left")

    #axs[0,1] = plt.subplot(112)
    axs[1].plot(plot_data[j][1], plot_data[j][3], label=f'{cycle_number_list[j]} cycles')
    axs[1].invert_xaxis()
    axs[1].invert_yaxis()
    axs[1].set_title('Median strain - Load')
    axs[1].legend(bbox_to_anchor=(1.04,1), loc="upper left")

    #axs[1,0] = plt.subplot(113)
    axs[2].plot(plot_data[j][1], plot_data[j][4], label=f'{cycle_number_list[j]} cycles')
    axs[2].invert_xaxis()
    axs[2].invert_yaxis()
    axs[2].set_title('Maximum strain - Load')
    axs[2].legend(bbox_to_anchor=(1.04,1), loc="upper left")

    for n in range(3):
        axs[3].plot(plot_data[j][1], plot_data[j][n+2], label=f'{cycle_number_list[j]} cycles')
        axs[3].invert_xaxis()
        axs[3].invert_yaxis()
        axs[3].set_title('Maximum strain - Load')
        axs[3].legend(bbox_to_anchor=(1.04, 1), loc="upper left")

for ax in axs.flat:
    ax.set(xlabel='Load [kN]', ylabel='Strain [Exx]')

fig.suptitle(f'Strain-Load Analysis of {select_specimen[0][5:9]}')
plt.show()

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



for i in range(5):
    select_specimen = files[i]
    export_list = {}

    df_data = import_data(select_specimen)

    df_separated = separate_sequences(df_data[0])
    df_separated.to_csv(f'separated_sequences_{select_specimen[0][5:9]}.csv')

    print('')
    print(select_specimen[0][5:9])

    # Make axial curve plot
    if i == 0:
        cycle_number_list_all = [500,  50500, 100500, 150500]
    elif i == 1:
        cycle_number_list_all = [500,  90500, 180500, 275500]
    elif i == 2:
        cycle_number_list_all = [500,  50500, 100500, 140500]
    elif i == 3:
        cycle_number_list_all = [500,  40500,  80500, 125500]
    elif i == 4:
        cycle_number_list_all = [500, 130500, 260500, 400500]

    linestyles = ['dotted', 'dashed', 'dashdot', 'solid']

    fig = plt.figure(figsize=(12, 9))
    plt.style.use('fivethirtyeight')
    fig.set_tight_layout(True)

    ax = plt.subplot()
    ax.clear()
    ax.set_xlim([0.02,-1.42])
    ax.set_ylim([1,-70])

    k = 0
    for i in range(len(cycle_number_list_all)):
        cycle_number_list = [cycle_number_list_all[i]]

        plot_data = axial_curve_data(cycle_number_list, df_separated, df_data[0])

        for j in range(len(cycle_number_list)):
            print(cycle_number_list[j])
            ax.plot(plot_data[j][2], plot_data[j][1], label = f'{cycle_number_list[j]} cycles', linestyle = linestyles[k])
            k += 1
            #ax.invert_xaxis()
            #ax.invert_yaxis()

    plt.xlabel('Displacement [mm]', fontsize=24)
    plt.ylabel('Load [kN]', fontsize=24)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    #plt.title(f'Load-displacement of {select_specimen[0][5:9]}')
    legend = plt.legend(loc='upper left', fontsize=26)

    #plt.savefig(f'Figures/{select_specimen[0][5:9]}/{"{:03d}".format(cycle_number_list_all[i])}.jpg')
    plt.savefig(f'Figures/MultiAxial/{select_specimen[0][5:9]}-multiple-axial-curves.jpg', transparent = True)

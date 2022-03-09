import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#
def min_max_displacement(df_seperated, df_data):
    cycle_number_list = df_seperated[0]
    min_deformation_list =[]
    max_deformation_list =[]

    for i in range(len(df_seperated)):
        min_def_n = df_seperated[1][i]-df_data[0][0]
        max_def_n = df_seperated[2][i]-df_data[0][0]
        min_def = df_data[2][min_def_n]
        max_def = df_data[2][max_def_n]
        min_deformation_list.append(min_def)
        max_deformation_list.append(max_def)

    plt.plot(min_deformation_list,cycle_number_list)
    plt.plot(max_deformation_list,cycle_number_list)
    plt.show()
    return

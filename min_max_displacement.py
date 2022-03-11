import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
def min_max_displacement(df_seperated, df_data):
    cycle_number_list = []
    min_deformation_list =[]
    max_deformation_list =[]
    count_lst =[]
    r_lst =[]

    for i in range(len(df_seperated)):
        min_def_n =int(df_seperated.iloc[ i,1] -df_data.iloc[0,0])
        max_def_n = int(df_seperated.iloc[i,2]-df_data.iloc[0,0])
        min_def = df_data.iloc[min_def_n,3]
        max_def = df_data.iloc[ max_def_n,3]
        cycle_number_list.append(df_seperated.iloc[ i,0])
        min_deformation_list.append(-min_def)
        max_deformation_list.append(-max_def)
        count_lst.append(df_seperated.iloc[i,1])

        x  = np.array(df_data.iloc[min_def_n:max_def_n,2])
        y  = np.array(df_data.iloc[min_def_n:max_def_n,3])
        #plt.plot(x,y)
        #plt.show()
        #xb = np.average(x)
        #yb = np.average(y)
        #r = np.sum((x-xb)*(y-yb))/(np.sum((x-xb)**2*(y-yb)**2))**0.5

        r = np.corrcoef(x, y)
        print(r[0][1])
        r_lst.append(r[0][1])


    fig, (ax1, ax2, ax3) = plt.subplots(3)
    #fig.suptitle('Vertically stacked subplots')
    fig.suptitle('A tale of 2 subplots this is the smaller one')
    #ax1.plot(x, y)
    #ax2.plot(x, -y)

    #plt.subplot(2, 1, 1)
    ax1.plot(cycle_number_list, min_deformation_list, 'ko-', linewidth=0)

    #ax1.ylabel('min deformation, mm')


    #ax2.subplot(2, 1, 2)
    ax2.plot(cycle_number_list, max_deformation_list, 'r.-', linewidth=0)
    #plt.xlabel('number of cycles')
    #ax2.ylabel('max deformation, mm')

    #ax3.subplot(2, 1, 3)
    ax3.plot(cycle_number_list, r_lst, 'r.-', linewidth=0)
    #ax3.xlabel('number of cycles')
    #ax3.ylabel('r')

    plt.show()
    #plt.plot()
    #plt.plot()
    #plt.show()
    return

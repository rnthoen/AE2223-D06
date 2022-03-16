import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def strain_load_curve_data(df_seperated, df_data):


    force = []
    strain1 = []
    strain2 = []
    strain3 = []

    i=70
    min_def_n =int(df_seperated.iloc[ i,1] -df_data[0].iloc[0,0])
    max_def_n = int(df_seperated.iloc[i,2]-df_data[0].iloc[0,0])

    if min_def_n%2==1:
        min_def_n=min_def_n+1
    x = np.zeros((10,(max_def_n-min_def_n)//2))

    for j in range(10):
        p=0
        for k in np.arange(min_def_n,max_def_n-1,2):
            if j==0:
                force.append(-df_data[0].iloc[k,2])
            idx1 = df_data[1]['File_Number'][df_data[1]['File_Number'] == k].index.tolist()

            x[j][p] = -df_data[1]["Eyy"].iloc[idx1[0]+90*j+10]
            p=p+1
        #strain1.append(-df_data[1]["Eyy"].iloc[idx1[0]+100])
        #strain2.append(-df_data[1]["Eyy"].iloc[idx1[0]+500])
        #strain3.append(-df_data[1]["Eyy"].iloc[idx1[0]+900])
    for z in range(10):
        plt.plot(force, x[z])
    #plt.plot(force, strain1)
    #plt.plot(force, strain2)
    #plt.plot(force, strain3)
    
    plt.show()
    return

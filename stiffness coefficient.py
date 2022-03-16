import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
def min_max_displacement(buckle,df_seperated, df_data):
    k1 =[]
    k2 =[]

    for i in range(len(df_seperated)):
        min_def_n =int(df_seperated.iloc[ i,1] -df_data.iloc[0,0])
        max_def_n = int(df_seperated.iloc[i,2]-df_data.iloc[0,0])
        buckle_def_n =  df_data[0]["load"][df_data[0]["load"] == buckle[i]].index.tolist()

        force_pre  = np.array(df_data.iloc[min_def_n:buckle_def_n,2])
        displacement_pre  = np.array(df_data.iloc[min_def_n:buckle_def_n,3])

        force_post  = np.array(df_data.iloc[min_def_n:buckle_def_n,2])
        displacement_post  = np.array(df_data.iloc[min_def_n:buckle_def_n,3])

        x = displacement_pre
        y = force_pre
        A = np.array([x, np.ones(len(x))])
        w1 = np.linalg.lstsq(A.T, y, rcond=None)[0][0]

        x = displacement_post
        y = force_post
        A = np.array([x, np.ones(len(x))])
        w2 = np.linalg.lstsq(A.T, y, rcond=None)[0][0]

        k1.append(w1)
        k2.append(w2)
    return k1,k2

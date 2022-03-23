import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
def stiffness(buckle,df_seperated, df_data):
    print("check 0")
    k1 =[]
    k2 =[]
    r_lst_pre=[]
    r_lst_post= []
    cycle_number_list = []

    for i in range(len(df_seperated)):
        if i%(len(df_seperated)//10)==0:
            print("progress"+str(i//(len(df_seperated)//10)))
        #'tuple' object has no attribute 'iloc'
        min_def_n =int(df_seperated.iloc[ i,1] -df_data.iloc[0,0])
        max_def_n = int(df_seperated.iloc[i,2]-df_data.iloc[0,0])

        buckle_def_n_lst = df_data[df_data["load"].apply(np.isclose,b=buckle[i], atol=1.0)].index.tolist()
        buckle_def_n_array = np.array(buckle_def_n_lst)
        #buckle_def_n = buckle_def_n[(buckle_def_n_array>=min_def_n)*(buckle_def_n_array<=max_def_n)]

        buckle_def_n_index =np.where(np.logical_and(buckle_def_n_array>=min_def_n, buckle_def_n_array<=max_def_n))
        buckle_def_n = buckle_def_n_array[buckle_def_n_index]
        #buckle_def_n =  df_data["load"][df_data["load"] == buckle[i]].index.tolist()
        cycle_number_list.append(df_seperated.iloc[ i,0])
        buckle_def_n = buckle_def_n[0]

        #print("check 2")

        force_pre  = np.array(df_data.iloc[min_def_n:buckle_def_n,2])
        displacement_pre  = np.array(df_data.iloc[min_def_n:buckle_def_n,3])

        force_post  = np.array(df_data.iloc[buckle_def_n:max_def_n,2])
        displacement_post  = np.array(df_data.iloc[buckle_def_n:max_def_n,3])
        #print("check 3")
        x = displacement_pre
        y = force_pre
        A = np.array([x, np.ones(len(x))])
        w1 = np.linalg.lstsq(A.T, y, rcond=None)[0][0]
        r = np.corrcoef(x, y)
        r_lst_pre.append(r[0][1])

        x = displacement_post
        y = force_post
        A = np.array([x, np.ones(len(x))])
        w2 = np.linalg.lstsq(A.T, y, rcond=None)[0][0]
        r = np.corrcoef(x, y)
        r_lst_post.append(r[0][1])



        k1.append(w1)
        k2.append(w2)
    #print("check 4")

    #print(k1)
    #print(k2)
    #print(len(k1))
    #print(len(k2))
    #print(df_seperated.iloc[0])
    #print(len(df_seperated.iloc[0]))
    specimin = "t"
    plt.subplot(3, 1, 1)
    plt.suptitle("stiffness coefficient "+specimin+", blue - pre buckled, red - post buckled, unit = [kN/mm] , note: not precise buckling values")
    plt.plot(cycle_number_list, k1, "b", marker = ".", linewidth=0,ms=2)
    plt.plot(cycle_number_list, k2, "r", marker = ".", linewidth=0,ms=2)
    plt.ylabel("both")
    plt.subplot(3, 1, 2)
    plt.plot(cycle_number_list, k1, "b", marker = ".", linewidth=0,ms=2)
    plt.ylabel("pre bucklings")
    plt.subplot(3, 1, 3)
    plt.plot(cycle_number_list, k2, "r", marker = ".", linewidth=0,ms=2)
    plt.ylabel("post buckling")
    plt.xlabel('number of cycles')
    plt.savefig("stiffness_coefficient_"+specimin+".svg")
    plt.show()

    plt.subplot(3, 1, 1)
    plt.suptitle("correlation "+specimin+", blue - pre buckled, red - post buckled, note: not precise buckling values")
    plt.plot(cycle_number_list, r_lst_pre, "b", marker = ".", linewidth=0,ms=2)
    plt.plot(cycle_number_list, r_lst_post, "r", marker = ".", linewidth=0,ms=2)
    plt.ylabel("both")
    plt.subplot(3, 1, 2)
    plt.plot(cycle_number_list, r_lst_pre, "b", marker = ".", linewidth=0,ms=2)
    plt.ylabel("pre bucklings")
    plt.subplot(3, 1, 3)
    plt.plot(cycle_number_list, r_lst_post, "r", marker = ".", linewidth=0,ms=2)
    plt.ylabel("post buckling")
    plt.xlabel('number of cycles')
    plt.savefig("correlation_"+specimin+".svg")
    plt.show()
    return k1,k2

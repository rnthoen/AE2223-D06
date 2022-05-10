import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Input specimen, cycles and parameter
specimen = 'L123'
parameter = 'W'
unit = 'mm'
threshold = 0.1

# Read data
# df = pd.read_csv(f'BucklingLoad/buckling_load_{specimen}_{parameter}_{threshold}.csv')
df_L103 = pd.read_csv(f'MTS_buckling/L103_MTS_buckling.csv')
df_L104 = pd.read_csv(f'MTS_buckling/L104_MTS_buckling.csv')
df_L105 = pd.read_csv(f'MTS_buckling/L105_MTS_buckling.csv')
df_L109 = pd.read_csv(f'MTS_buckling/L109_MTS_buckling.csv')
df_L123 = pd.read_csv(f'MTS_buckling/L123_MTS_buckling.csv')
df_L103_DIC = pd.read_csv(f'BucklingLoad/buckling_load_L103_W_0.1.csv')
df_L104_DIC = pd.read_csv(f'BucklingLoad/buckling_load_L104_W_0.1.csv')
df_L105_DIC = pd.read_csv(f'BucklingLoad/buckling_load_L105_W_0.1.csv')
df_L109_DIC = pd.read_csv(f'BucklingLoad/buckling_load_L109_W_0.1.csv')
df_L123_DIC = pd.read_csv(f'BucklingLoad/buckling_load_L123_W_0.2.csv')

### Calculate lower and upper limits
# low_limit_1 = []
# upp_limit_1 = []
# low_limit_2 = []
# upp_limit_2 = []
# for i in range(len(df.cycle_number)):
#     low_limit_1.append(df.buckling_load[i] + df.stdev[i])
#     upp_limit_1.append(df.buckling_load[i] - df.stdev[i])
#     low_limit_2.append(df.buckling_load[i] + 2 * df.stdev[i])
#     upp_limit_2.append(df.buckling_load[i] - 2 * df.stdev[i])


# Plot results
fig = plt.figure(figsize=(12, 8))
fig.set_tight_layout(True)

ax = plt.subplot()
# ax.fill_between(df.cycle_number, low_limit_1, upp_limit_1, color = 'blue', zorder = 0, alpha = 0.3, label = f'68% interval')
# ax.fill_between(df.cycle_number, low_limit_1, low_limit_2, color = 'green', zorder = 1, alpha = 0.3, label = f'95% interval')
# ax.fill_between(df.cycle_number, upp_limit_1, upp_limit_2, color = 'green', zorder = 1, alpha = 0.3)


# ax.plot(df_L103_DIC.cycle_number, df_L103_DIC.buckling_load, label = f'L1-03 (DIC)', linewidth = 3, zorder = 4, color = 'green')
# ax.plot(df_L103.cycle_number, df_L103.buckling_load, label = f'L1-03 (MTS)', linewidth = 3, zorder = 4, color = 'red')
# ax.plot(df_L103.cycle_number, df_L103.buckling_load_new, label = f'L1-03 (MTS NEW!)', linewidth = 3, zorder = 4, color = 'blue')

# ax.plot(df_L104_DIC.cycle_number, df_L104_DIC.buckling_load, label = f'L1-04 (DIC)', linewidth = 3, zorder = 5, color = 'green')
# ax.plot(df_L104.cycle_number, df_L104.buckling_load, label = f'L1-04 (MTS)', linewidth = 3, zorder = 5, color = 'red')
# ax.plot(df_L104.cycle_number, df_L104.buckling_load_new, label = f'L1-04 (MTS NEW!)', linewidth = 3, zorder = 5, color = 'blue')

# ax.plot(df_L105_DIC.cycle_number, df_L105_DIC.buckling_load, label = f'L1-05 (DIC)', linewidth = 3, zorder = 6, color = 'green')
# ax.plot(df_L105.cycle_number, df_L105.buckling_load, label = f'L1-05 (MTS)', linewidth = 3, zorder = 6, color = 'red')
# ax.plot(df_L105.cycle_number, df_L105.buckling_load_new, label = f'L1-05 (MTS NEW!)', linewidth = 3, zorder = 6, color = 'blue')

# ax.plot(df_L109_DIC.cycle_number, df_L109_DIC.buckling_load, label = f'L1-09 (DIC)', linewidth = 3, zorder = 7, color = 'green')
# ax.plot(df_L109.cycle_number, df_L109.buckling_load, label = f'L1-09 (MTS)', linewidth = 3, zorder = 7, color = 'red')
# ax.plot(df_L109.cycle_number, df_L109.buckling_load_new, label = f'L1-09 (MTS NEW!)', linewidth = 3, zorder = 7, color = 'blue')

ax.plot(df_L123_DIC.cycle_number, df_L123_DIC.buckling_load, label = f'L1-23 (DIC)', linewidth = 3, zorder = 3, color = 'green')
ax.plot(df_L123.cycle_number, df_L123.buckling_load, label = f'L1-23 (MTS)', linewidth = 3, zorder = 3, color = 'red')
ax.plot(df_L123.cycle_number, df_L123.buckling_load_new, label = f'L1-23 (MTS NEW!)', linewidth = 3, zorder = 3, color = 'blue')

# ax.plot(df_L104.cycle_number, df_L104.buckling_load, label = f'L104', linewidth = 3, zorder = 5)
# ax.plot(df_L105.cycle_number, df_L105.buckling_load, label = f'L105', linewidth = 3, zorder = 6)
# ax.plot(df_L109.cycle_number, df_L109.buckling_load, label = f'L109', linewidth = 3, zorder = 7)
# ax.plot(df_L123.cycle_number, df_L123.buckling_load, label = f'L123', linewidth = 3, zorder = 3)

ax.set_xticks(np.arange(0, list(df_L123.cycle_number)[-1], 50000))
ax.invert_yaxis()
ax.grid(True)

plt.ylim(-9, -41)

plt.title('Buckling force from MTS data')
plt.xlabel('Cycles [-]')
plt.ylabel('Buckling force [kN]')
plt.legend()
# plt.savefig(f'BucklingLoad/buckling_load_{specimen}_{parameter}_{threshold}.svg')
plt.savefig(f'MTS_buckling/MTS_buckling.svg')
plt.show()

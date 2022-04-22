import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Input specimen, cycles and parameter
specimen = 'L103'
parameter = 'W'
unit = 'mm'
threshold = 0.1

# Read data
df = pd.read_csv(f'BucklingLoad/buckling_load_{specimen}_{parameter}_{threshold}.csv')

# Calculate lower and upper limits
low_limit_1 = []
upp_limit_1 = []
low_limit_2 = []
upp_limit_2 = []
for i in range(len(df.cycle_number)):
    low_limit_1.append(df.buckling_load[i] + df.stdev[i])
    upp_limit_1.append(df.buckling_load[i] - df.stdev[i])
    low_limit_2.append(df.buckling_load[i] + 2 * df.stdev[i])
    upp_limit_2.append(df.buckling_load[i] - 2 * df.stdev[i])


# Plot results
fig = plt.figure(figsize=(12, 8))
fig.set_tight_layout(True)

ax = plt.subplot()
ax.fill_between(df.cycle_number, low_limit_1, upp_limit_1, color = 'blue', zorder = 0, alpha = 0.3, label = f'68% interval')
ax.fill_between(df.cycle_number, low_limit_1, low_limit_2, color = 'green', zorder = 1, alpha = 0.3, label = f'95% interval')
ax.fill_between(df.cycle_number, upp_limit_1, upp_limit_2, color = 'green', zorder = 1, alpha = 0.3)

ax.plot(df.cycle_number, df.buckling_load, label = f'F_buckle (Δ{parameter}, {threshold} {unit})', color = 'black', zorder = 2, linewidth = 3)

ax.set_xticks(np.arange(0, list(df.cycle_number)[-1], 10000))
ax.invert_yaxis()
ax.grid(True)

plt.ylim(-4, -26)

plt.title(f'{specimen}')
plt.xlabel('N_cycles [-]')
plt.ylabel('F_buckle [kN]')
plt.legend()
plt.savefig(f'BucklingLoad/buckling_load_{specimen}_{parameter}_{threshold}.svg')
plt.show()

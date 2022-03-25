import pandas as pd
import matplotlib.pyplot as plt

# Input specimen, cycles and parameter
specimen = 'L104'
parameter = 'W'
unit = 'mm'
threshold = 0.1

# Read data
df = pd.read_csv(f'buckling_load_{specimen}.csv')

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
ax.fill_between(df.cycle_number, low_limit_2, upp_limit_2, color = 'green', zorder = 1, alpha = 0.3, label = f'95% interval')
ax.fill_between(df.cycle_number, low_limit_1, upp_limit_1, color = 'blue', zorder = 0, alpha = 0.3, label = f'68% interval')

ax.plot(df.cycle_number, df.buckling_load, label = 'F_buckle', color = 'black', zorder = 2, linewidth = 3)
ax.invert_yaxis()

plt.ylim(-4, -26)

plt.title(f'F_buckle of {specimen} (Δ{parameter} = {threshold} [{unit}])')
plt.xlabel('Cycles [-]')
plt.ylabel('F_buckle [kN]')
plt.legend()
plt.savefig(f'buckling_load_{specimen}.png')
plt.show()

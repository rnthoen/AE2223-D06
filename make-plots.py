"""
Organize data into dataframes
"""

files = ['Data/L103/L1-03.csv',
         'Data/L104/L1-04.csv',
         'Data/L105/L1-05.csv',
         'Data/L109/L1-09.csv',
         'Data/L123/L1-23.csv',
]

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read CSV data
select_file = files[4]
df = pd.read_csv(select_file)

# Select data to plot
time = np.array((df["Time_0"]))             # [s]
load = np.array(df["Dev2/ai0"] * 10)        # [kN]
x_displ = np.array(df["Dev2/ai1"] * 0.75)   # [mm]

# Trim ends for L103
if select_file == files[0]:
    start = 44
    end = -3
# Trim ends for L104
elif select_file == files[1]:
    start = 37
    end = -5
# Trim ends for L105
elif select_file == files[2]:
    start = 38
    end = -5
# Trim ends for L109
elif select_file == files[3]:
    start = 35
    end = -4
# Trim ends for L123
elif select_file == files[4]:
    start = 814
    end = -4878

i = start
cycles = 500
new_sequence_time = []
new_sequence_load = []

split_data = []

while i < (len(load) + end):
    if load[i] > (load[i-1] + 10):
        new_sequence_time.append(time[i])
        new_sequence_load.append(load[i])

        sequence = {"cycles": cycles, "count_start": df.at[i, "Count"], "count_end": 0}
        split_data.append(sequence)

        # TODO: Update end of previous sequence
        if len(split_data) > 1:
            split_data[-2]["count_end"] += split_data[-1]["count_start"] - 1

        cycles += 500
        if cycles % 5000 == 0:
            cycles += 500
    i += 1

# Update last data point
split_data[-1]["count_end"] = len(load) + end + 1


# Calculate number of data points in sequence
length = [[], []]
for sequence in split_data:
    sequence_length = sequence["count_end"] - sequence["count_start"]
    if sequence_length < 1000:
        length[0].append(sequence["cycles"])
        length[1].append(sequence_length)

# Calculate duration of sequence
duration = [[], []]
for sequence in split_data:
    sequence_duration = time[sequence["count_end"]] - time[sequence["count_start"]]
    duration[0].append(sequence["cycles"])
    duration[1].append(sequence_duration)

# Make a plot
plt.style.use("fivethirtyeight")

fig, ax1 = plt.subplots(figsize = (16,9))
fig.set_tight_layout(True)

# plt.scatter(time[start:end], load[start:end])
# plt.scatter(new_sequence_time, new_sequence_load)
# plt.xlabel("Time [s]")
# plt.ylabel("Applied load [kN]")
# plt.title(f"Test Sequences Separated ({select_file[-25:]})")

ax1.scatter(length[0], length[1], color = "blue", alpha = 0.8)
ax1.set_xlabel("Cycles [-]")
ax1.set_ylabel("Data points [-]", color = "blue")
ax2 = ax1.twinx()
ax2.scatter(duration[0][:-1], duration[1][:-1], color = "red", alpha = 0.8)
ax2.set_ylabel("Duration [s]", color = "red")
plt.title(f"Data Points and Duration of Test Sequence ({select_file[-25:]})")
print(len(time))
plt.show()

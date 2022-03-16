import pandas as pd
import matplotlib.pyplot as plt


coordinates = [
    [2, 5],
    [0, 1],
    [1, 5],
    [4, 3]
]

colormap = 'coolwarm'
#[3, 4, 3, 5]


def heatmap_plot_imshow(coordinates, colormap):
    plt.imshow(coordinates, cmap = colormap)

heatmap_plot_imshow(coordinates, colormap)
plt.show()

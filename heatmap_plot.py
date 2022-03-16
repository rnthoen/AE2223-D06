import pandas as pd
import matplotlib.pyplot as plt
from heatmap_data import heatmap_data

def heatmap_plot(plot_data, point_size, colormap, color_label, plot_title, filename, range):
    var1 = plot_data[0]
    var2 = plot_data[1]
    colors = plot_data[2]

    fig = plt.figure(figsize=(8, 8))
    fig.set_tight_layout(True)

    plt.scatter(var1, var2, s = point_size, c = colors, cmap = colormap)
    c = plt.colorbar(label = color_label)
    plt.clim(range[0], range[1])
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.title(plot_title)

    plt.savefig(filename)

    #plt.show()

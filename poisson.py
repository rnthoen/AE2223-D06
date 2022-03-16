from interpolate_panel import interpolate_panel
import numpy as np
from heatmap_plot import heatmap_plot
import matplotlib.pyplot as plt


def poisson(df_data, N, specimen, cycle_number):
    DIC_df = df_data[1]
    MTS_df = df_data[0]
    # grid_y = np.linspace(-70, 70, 200)
    # grid_x = x * np.ones(len(grid_y))
    grid_x, grid_y = np.mgrid[-80:80:200j, -110:110:200j]
    strain_x = interpolate_panel(DIC_df, N, grid_x, grid_y, "Exx")
    strain_y = interpolate_panel(DIC_df, N, grid_x, grid_y, "Eyy")
    poisson_ratio = -strain_x/strain_y
    load = MTS_df.loc[MTS_df['count'] == N]["load"].iloc[0]

    # create poisson heat map
    plot_data = np.vstack((grid_x.flatten(), grid_y.flatten(), poisson_ratio.flatten()))
    point_size = 20
    range = (min(poisson_ratio.flatten()), max(poisson_ratio.flatten()))
    # range = (-1, 1)
    colormap = 'rainbow'
    color_label = 'poisson [-]'
    plot_title = f'{specimen}, {load} kN, count = {N}, cycle number = {cycle_number}'
    filename = f'Heatmap/{specimen}_{N}.jpg'
    heatmap_plot(plot_data, point_size, colormap, color_label, plot_title, filename, range)
    plt.axvline(x=-32.5, color='k', linestyle='--')
    plt.axvline(x=32.5, color='k', linestyle='--')
    plt.show()


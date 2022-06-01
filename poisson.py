from interpolate_panel import interpolate_panel
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable


def poisson(df_data, counts, specimen, cycle_numbers, path):
    """ Generate poisson heat maps at given cycle number and load (depending on specified count numbers)
        - df_data: contains DIC and MTS data for given panel
        - counts: 'count' numbers (moment in time) at which poisson ratio is calculated
        - speciment: specimen for which poisson ratio is calculated
        - cycle_numbers: list of cycle numbers at which the poisson ratio is calculated
        This function generates poisson heat maps at the cycle numbers specified in the cycle_numbers list for a given
        specimen depending on the data included in the df_data. Path is where the graphs are saved
    """
    DIC_df = df_data[1]                                     # panel DIC data
    MTS_df = df_data[0]                                     # panel MTS data
    grid_x, grid_y = np.mgrid[-75:75:200j, -70:70:200j]     # create grid of points to calculate poisson's ratio at
    i = 0

    # configure plots
    cmap = plt.get_cmap("rainbow")
    fig, axes = plt.subplots(1, len(counts), sharey=True, figsize=(20, 10), constrained_layout=True)

    for ax in axes:
        count = counts[i]                                                   # corresponds to given load
        cycle_number = cycle_numbers[i]                                     # given cycle number

        strain_x = interpolate_panel(DIC_df, count, grid_x, grid_y, "Exx")
        strain_y = interpolate_panel(DIC_df, count, grid_x, grid_y, "Eyy")
        poisson_ratio = -strain_x/strain_y                                  # grid of poisson values
        load = MTS_df.loc[MTS_df['count'] == count]["load"].iloc[0]         # retrieve load for given count

        # create poisson heat map
        plot_data = np.vstack((grid_x.flatten(), grid_y.flatten(), poisson_ratio.flatten()))
        point_size = 20
        colormap = 'rainbow'
        color_label = 'poisson ratio [-]'
        plot_title = f'{specimen}, {round(load, 1)} kN, count = {count}, cycle number = {cycle_number}'

        ax.scatter(plot_data[0], plot_data[1], s=point_size, c=plot_data[2], cmap=colormap, vmin=-0.5, vmax=1.4)
        axes[0].set_ylabel('y [mm]', fontsize=20)
        ax.set_xlabel('x [mm]', fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=20)
        # ax.title.set_text(plot_title)
        ax.axvline(x=-32.5, color='k', linestyle='--')                      # indicate bounds of stiffener
        ax.axvline(x=32.5, color='k', linestyle='--')

        i += 1

    filename = f'Poisson/{path}/{specimen}_{round(load, 1)}_{count}.jpg'

    norm = plt.Normalize(-0.5, 1.4)
    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes)
    cbar.ax.set_title(color_label, fontsize=20)
    cbar.ax.tick_params(axis='both', which='major', labelsize=20)

    plt.savefig(filename)                                                   # save graph


def poisson_avg(df_data, count, x_bounds, y_bounds):
    """ Generate poisson heat maps at given cycle number and load (depending on specified count numbers)
        - df_data: contains DIC and MTS data for given panel
        - count: 'count' number (moment in time) at which poisson ratio is calculated
        - x_bounds: list of upper and lower bounds for the x-value
        - y_bounds: list of upper and lower bounds for the y-value
        This function generates the average poisson ratio over patches of the panel as specified in the x- and y-bounds
    """
    DIC_df = df_data[1]  # panel DIC data

    avg_poissons = []
    for x_bound, y_bound in zip(x_bounds, y_bounds):
        grid_x, grid_y = np.mgrid[x_bound[0]:x_bound[1]:200j, y_bound[0]:y_bound[1]:200j]  # create grid of points to calculate poisson's ratio at

        strain_x = interpolate_panel(DIC_df, count, grid_x, grid_y, "Exx")
        strain_y = interpolate_panel(DIC_df, count, grid_x, grid_y, "Eyy")
        poisson_ratio = -strain_x / strain_y

        avg_poissons.append(np.average(poisson_ratio))                                      # take average of poisson grid

    return avg_poissons
from interpolate_panel import interpolate_panel
import numpy as np
import matplotlib.pyplot as plt


def poisson(df_data, x, N):
    DIC_df = df_data[1]
    MTS_df = df_data[0]
    # grid_y = np.linspace(-70, 70, 200)
    # grid_x = x * np.ones(len(grid_y))
    grid_x, grid_y = np.mgrid[-65:65:200j, -70:70:200j]
    strain_x = interpolate_panel(DIC_df, N, grid_x, grid_y, "Exx")
    strain_y = interpolate_panel(DIC_df, N, grid_x, grid_y, "Eyy")
    poisson_ratio = -strain_x/strain_y
    print("Load: ", MTS_df.loc[MTS_df['count'] == N]["load"].iloc[0])
    print(poisson_ratio.shape)
    plt.scatter(np.linspace(-65, 65, 200), np.linspace(-70, 70, 200), s=200, c=poisson_ratio, cmap='gray')
    plt.show()



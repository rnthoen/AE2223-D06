import numpy as np
from scipy import interpolate as interpol


def interpolate_panel(DIC_df, N, grid_x, grid_y, variable):
    """ Interpolate certain value on a grid of x-y values
        - DIC_df: datafram containing all DIC data
        - N: File_Number at which to interpolate
        - grid_x: x-coordinates at which to interpolate (nxm)
        - grid_y: x-coordinates at which to interpolate (nxm)
    """
    df_seq = DIC_df.loc[DIC_df['File_Number'] == N]
    points = np.vstack([df_seq["X"], df_seq["Y"]]).transpose()
    values = np.array(df_seq[variable])
    grid_values = interpol.griddata(points, values, (grid_x, grid_y), method='nearest', rescale=False)
    return grid_values

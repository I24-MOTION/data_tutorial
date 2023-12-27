def visualize_heatmap(speed_data, starttime, endtime, dx, dt, fig_width=8, fig_height=8, minor_xtick=150,
                      colors=None, cmap='green_to_red',min_milemarker = 58.7, testbed_mile = 4):
    """
    Visualizes a heatmap of speed data over time and mile markers.

    Parameters:
    -----------
    speed_data : DataFrame
        A DataFrame containing speed data with columns 't', 'x', and 'speed'.
    starttime : int
        The starting time in seconds in Unix time.
    endtime : int
        The ending time in seconds in Unix time.
    dx (float):
        The spatial resolution (the spatial size for the Edie's box).
    dt (float):
        The temporal resolution (the temporal size for the Edie's box).
    fig_width : int, optional
        The width of the generated figure in inches. Default is 8.
    fig_height : int, optional
        The height of the generated figure in inches. Default is 8.
    minor_xtick : int, optional
        The interval between minor x-axis ticks in seconds. Default is 150.
    colors : list of colors, optional
        A list of colors for the heatmap. Default is unspecified.
    cmap : colormap, optional
        The colormap to use for the heatmap. Default is 'green_to_red'.

    Returns:
    --------
    None
        This function generates and displays a heatmap plot but does not return any value.

    Notes:
    ------
    This function uses matplotlib to create a heatmap visualization of speed data along mile markers and time intervals.
    It displays speed data as a colormap with color-coded speed values, and mile markers and time intervals are marked
    on the axes. The colormap can be customized using the `colors` and `cmap` parameters.

    Example:
    --------
    visualize_heatmap(speed_data, starttime=0, endtime=3600, dx=0.01, dt=60)

    This example will create a heatmap plot of `speed_data` with specified parameters.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    import matplotlib.style as mplstyle
    import datetime
    jet = plt.cm.jet
    colors = [jet(x) for x in np.linspace(1, 0.5, 256)]
    # green_to_red is my favirate colormap...
    green_to_red = LinearSegmentedColormap.from_list('GreenToRed', colors, N=256)
    plt.figure(figsize=(fig_width, fig_height))
    plt.rc('font', family='serif', size=25)
    sc = plt.scatter(speed_data.t, speed_data.x, c=speed_data.speed, cmap=green_to_red, vmin=0, vmax=80, marker='s', s=5)
    plt.gca().invert_yaxis()
    start_time = datetime.datetime.strptime(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M"), "%H:%M")
    yticks = list(range(0, int(testbed_mile/dx) + 1, int(testbed_mile/dx/4)))
    ticks = list(range(0, endtime-starttime + 1, minor_xtick))
    ylabels = [dx * tick + min_milemarker for tick in yticks]
    plt.yticks(yticks, labels=ylabels, rotation=0)
    plt.ylabel('Mile Marker')
    plt.xlabel(datetime.datetime.fromtimestamp(starttime).strftime("%Y-%m-%d"))
    xlabels = [(start_time + dt * datetime.timedelta(seconds=tick)).strftime("%H:%M") for tick in ticks]
    plt.xticks(ticks, labels=xlabels, rotation=0)
    plt.xlim(0, (endtime-starttime)/dt)
    plt.grid(which='both', linewidth=2, linestyle='--')
    plt.colorbar(sc, pad=0.01).set_label('Speed (mph)', rotation=90, labelpad=20)
    plt.show()


def visualize_heatmap_vt(speed_data, vt, starttime, endtime, dx, dt, fig_width=8, fig_height=8, minor_xtick=150,
                      colors=None, cmap='green_to_red',min_milemarker = 58.7, testbed_mile = 4):
    """
    Visualizes a heatmap of speed data over time and mile markers.

    Parameters:
    -----------
    speed_data : DataFrame
        A DataFrame containing speed data with columns 't', 'x', and 'speed'.
    starttime : int
        The starting time in seconds in Unix time.
    endtime : int
        The ending time in seconds in Unix time.
    dx (float):
        The spatial resolution (the spatial size for the Edie's box).
    dt (float):
        The temporal resolution (the temporal size for the Edie's box).
    fig_width : int, optional
        The width of the generated figure in inches. Default is 8.
    fig_height : int, optional
        The height of the generated figure in inches. Default is 8.
    minor_xtick : int, optional
        The interval between minor x-axis ticks in seconds. Default is 150.
    colors : list of colors, optional
        A list of colors for the heatmap. Default is unspecified.
    cmap : colormap, optional
        The colormap to use for the heatmap. Default is 'green_to_red'.

    Returns:
    --------
    None
        This function generates and displays a heatmap plot but does not return any value.

    Notes:
    ------
    This function uses matplotlib to create a heatmap visualization of speed data along mile markers and time intervals.
    It displays speed data as a colormap with color-coded speed values, and mile markers and time intervals are marked
    on the axes. The colormap can be customized using the `colors` and `cmap` parameters.

    Example:
    --------
    visualize_heatmap(speed_data, starttime=0, endtime=3600, dx=0.01, dt=60)

    This example will create a heatmap plot of `speed_data` with specified parameters.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    import matplotlib.style as mplstyle
    import datetime
    jet = plt.cm.jet
    colors = [jet(x) for x in np.linspace(1, 0.5, 256)]
    # green_to_red is my favirate colormap...
    green_to_red = LinearSegmentedColormap.from_list('GreenToRed', colors, N=256)
    plt.figure(figsize=(fig_width, fig_height))
    plt.rc('font', family='serif', size=25)
    sc = plt.scatter(speed_data.t, speed_data.x, c=speed_data.speed, cmap=green_to_red, vmin=0, vmax=80, marker='s', s=5)
    plt.scatter(vt.time/dt, (vt.space-58.7)/dx, c='black', s=1)
    plt.gca().invert_yaxis()
    start_time = datetime.datetime.strptime(datetime.datetime.fromtimestamp(starttime).strftime("%H:%M"), "%H:%M")
    yticks = list(range(0, int(testbed_mile/dx) + 1, int(testbed_mile/dx/4)))
    ticks = list(range(0, endtime-starttime + 1, minor_xtick))
    ylabels = [dx * tick + min_milemarker for tick in yticks]
    plt.yticks(yticks, labels=ylabels, rotation=0)
    plt.ylabel('Mile Marker')
    plt.xlabel(datetime.datetime.fromtimestamp(starttime).strftime("%Y-%m-%d"))
    xlabels = [(start_time + dt * datetime.timedelta(seconds=tick)).strftime("%H:%M") for tick in ticks]
    plt.xticks(ticks, labels=xlabels, rotation=0)
    plt.xlim(0, (endtime-starttime)/dt)
    plt.grid(which='both', linewidth=2, linestyle='--')
    plt.colorbar(sc, pad=0.01).set_label('Speed (mph)', rotation=90, labelpad=20)
    plt.show()
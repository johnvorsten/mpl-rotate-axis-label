# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 20:16:22 2020

See the matplotlib axis3d source for some of the projection code I took
Specifically, I reused existing code to get the current dimensions of
the displayed figure. Then, the dimensions and position of the Axis within
the figure is found.  A projection of the Axis onto the users screen
is found, and from there the rotation of the axis with respect to the users
horizontal is calculated

See https://matplotlib.org/_modules/mpl_toolkits/mplot3d/axis3d.html

@author: z003vrzk
"""
# Python imports

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d, proj3d
from mpl_toolkits.mplot3d.axis3d import get_flip_min_max


#%%

class RotateTickLabel:
    def __init__(self, axis, axes):
        """
        Rotate a set of axis labels relative to the axis
        Hold state information (axis) to define which axis ticklabels should
        be redrawn
        inputs
        -------
        axis : (mpl_toolkits.mplot3d.axis3d.Axis) This is the Axis object
            you want to rotate tick labels to. It is NOT the AXES object -
            see the plot example for what to pass
        axes : (mpl_toolkits.mplot3d.axes3d.Axes3D) This is the Axes object
            that is probably a subplot of a figure. See the plot
            example below for arguments to pass"""
        self.axis = axis
        self.axes = axes
        self.cid = axes.figure.canvas.mpl_connect('draw_event', self)

    def __call__(self, event):
        print('Draw Event', event) # TODO Remove when used
        self.set_axis_label_rotate(event)

    def set_axis_label_rotate(self, event):
        """Rotate a set of axis labels relative to the axis
        inputs
        -------
        event : (matplotlib.backend_bases.DrawEvent)
        https://matplotlib.org/3.2.2/api/backend_bases_api.html#matplotlib.backend_bases.DrawEvent"""

        # Setup
        renderer = event.renderer
        axes = self.axes # Axes - includes axes.xaxis and axes.yaxis
        axis = self.axis # Axis

        info = axis._axinfo
        mins, maxs, centers, deltas, tc, highs = axis._get_coord_info(renderer)

        # Determine grid lines
        minmax = np.where(highs, maxs, mins)

        # Draw main axis line
        juggled = info['juggled']
        edgep1 = minmax.copy()
        edgep1[juggled[0]] = get_flip_min_max(edgep1, juggled[0], mins, maxs)

        edgep2 = edgep1.copy()
        edgep2[juggled[1]] = get_flip_min_max(edgep2, juggled[1], mins, maxs)
        pep = proj3d.proj_trans_points([edgep1, edgep2], renderer.M)

        # Draw labels
        # The transAxes transform is used because the Text object
        # rotates the text relative to the display coordinate system.
        # Therefore, if we want the labels to remain parallel to the
        # axis regardless of the aspect ratio, we need to convert the
        # edge points of the plane to display coordinates and calculate
        # an angle from that.
        peparray = np.asanyarray(pep)
        dx, dy = (axes.axes.transAxes.transform([peparray[0:2, 1]]) -
                  axes.axes.transAxes.transform([peparray[0:2, 0]]))[0]

        # Rotate label
        for tick_label in axis.get_majorticklabels():
            angle = art3d._norm_text_angle(np.rad2deg(np.arctan2(dy, dx)))
            tick_label.set_rotation(angle)

        return None



def rotate_tick_label(event):
    """This is a simple method to rotate only one group of axis labels
    relative to the axis. It does not have the abaility to hold state
    An option is to use a factor function to hold state, but this is a
    simple example that works
    inputs
    -------
    event : (matplotlib.backend_bases.DrawEvent)
    https://matplotlib.org/3.2.2/api/backend_bases_api.html#matplotlib.backend_bases.DrawEvent"""

    # Setup
    renderer = event.renderer
    axes = event.canvas.figure.axes[0]

    # renderer.open_group('axis3d')

    info = axes.yaxis._axinfo
    mins, maxs, centers, deltas, tc, highs = axes.yaxis._get_coord_info(renderer)

    # Determine grid lines
    minmax = np.where(highs, maxs, mins)

    # Draw main axis line
    juggled = info['juggled']
    edgep1 = minmax.copy()
    edgep1[juggled[0]] = get_flip_min_max(edgep1, juggled[0], mins, maxs)

    edgep2 = edgep1.copy()
    edgep2[juggled[1]] = get_flip_min_max(edgep2, juggled[1], mins, maxs)
    pep = proj3d.proj_trans_points([edgep1, edgep2], renderer.M)

    # Draw labels
    peparray = np.asanyarray(pep)
    dx, dy = (axes.axes.transAxes.transform([peparray[0:2, 1]]) -
              axes.axes.transAxes.transform([peparray[0:2, 0]]))[0]

    # Rotate label
    for tick_label in axes.yaxis.get_majorticklabels():
        angle = art3d._norm_text_angle(np.rad2deg(np.arctan2(dy, dx)))
        tick_label.set_rotation(angle)

    return None



def plot_integral():
    """
    inputs
    -------
    incomes : (list) of Income objects
    start_date : (datetime.date)
    end_date : (datetime.date)
    smooth : (bool)
    outputs
    -------

    """

    x = np.arange(-np.pi, np.pi, 0.25)
    y = np.arange(-10, 10, 0.5)
    xy, yx = np.meshgrid(x,y)
    z = np.cos(xy)

    # X labels
    num_ticks = 4
    tick_index = np.linspace(0, x.shape[0]-1, num=num_ticks, dtype=np.int16)
    xticks = x[tick_index]
    xlabels = ['x_{:.1f}'.format(x) for x in xticks]
    # Y labels
    yticks = [ y[y.shape[0]//2] ]
    ylabels = ['-10 → +10']

    """3-dimensional plotting - y & x axis showoff"""
    fig3d = plt.figure(1)
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.set_title('Y Axis with labels rotated parallel to axis')
    surf = ax3d.plot_surface(xy, yx, z, cmap='summer', linewidth=0,
                           antialiased=False)
    # Label X axis
    ax3d.set_xticks(xticks)
    ax3d.set_xticklabels(xlabels)
    # Label y axis
    ax3d.set_yticks(yticks)
    ax3d.set_yticklabels(ylabels)
    # Connect event to rotate probability axis label
    fig3d.canvas.mpl_connect('draw_event', rotate_tick_label) # Simple method
    # Flexible method
    rotateTickLabel = RotateTickLabel(ax3d.xaxis, ax3d)
    fig3d.canvas.mpl_connect('draw_event', rotateTickLabel)

    # Label axis
    ax3d.set_xlabel('X Values []', labelpad=10)
    ax3d.set_ylabel('Y Values []', labelpad=10)
    ax3d.set_zlabel('Z Values []', labelpad=10)

    ax3d.view_init(elev=20, azim=125) #elev is in z plane, azim is in x,y plane

    plt.show()

    return None


if __name__ == '__main__':
    plot_integral()


#%% Play

if __name__ == '__DontExecute':
    fig3d = plt.figure(1)
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.set_title('Axes Title')
    ax3d.set_xlim(0,5)
    ax3d.set_ylim(0,5)

    # Label X axis
    ax3d.set_xticks([1])
    ax3d.set_xticklabels(['Non-rotated Label\n"left,top"'])
    ax3d.xaxis.get_majorticklabels()[0].set_verticalalignment('top')
    ax3d.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
    # ax3d.xaxis.get_majorticklabels()[0].set_rotation(0)
    # Label y axis
    ax3d.set_yticks([1])
    ax3d.set_yticklabels(['Rotated Label'])
    ax3d.yaxis.get_majorticklabels()[0].set_rotation(45)

    # Label axis
    ax3d.set_xlabel('X Axis', labelpad=20)
    ax3d.set_ylabel('Y Axis', labelpad=20)
    ax3d.set_zlabel('Z Axis', labelpad=20)
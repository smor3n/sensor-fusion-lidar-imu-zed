#!/usr/bin/env python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rospkg
from math import *


def f_plot(*args, **kwargs):
    xlist = []
    ylist = []
    for i, arg in enumerate(args):
        if (i % 2 == 0):
            xlist.append(arg)
        else:
            ylist.append(arg)

    colors = kwargs.pop('colors', 'k')
    linewidth = kwargs.pop('linewidth', 1.)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    i = 0
    for x, y, color in zip(xlist, ylist, colors):
        i += 1
        ax.plot(x, y, color=color, linewidth=linewidth, label=str(i))

    ax.grid(True)
    ax.legend()


# get an instance of RosPack with the default search paths
rospack = rospkg.RosPack()

# get the file path for sensor_fusion
rospack.get_path('sensor_fusion')

path = rospack.get_path('sensor_fusion') + '/dataTxt/laps/'

data_pose = np.loadtxt(path + "pose_position.txt", delimiter=' ', dtype=np.float)
data_lidar_odom = np.loadtxt(path + "pose_orientation.txt", delimiter=' ', dtype=np.float)
colors = ['red', 'blue', 'green']

t_pose = data_pose[:, 0]
x_pose = data_pose[:, 1]
y_pose = data_pose[:, 2]
yaw_pose = data_lidar_odom[:, 1]

t = t_pose
x = x_pose

dx = np.zeros(x.shape, np.float)
dx[0:-1] = np.diff(x) / np.diff(t)
dx[-1] = (x[-1] - x[-2]) / (t[-1] - t[-2])

vx = dx

ddx = np.zeros(dx.shape, np.float)
ddx[0:-1] = np.diff(dx) / np.diff(t)
ddx[-1] = (dx[-1] - dx[-2]) / (t[-1] - t[-2])

t = t_pose
y = y_pose

dy = np.zeros(y.shape, np.float)
dy[0:-1] = np.diff(y) / np.diff(t)
dy[-1] = (y[-1] - y[-2]) / (t[-1] - t[-2])

vy = dy

ddy = np.zeros(dy.shape, np.float)
ddy[0:-1] = np.diff(dy) / np.diff(t)
ddy[-1] = (dy[-1] - dy[-2]) / (t[-1] - t[-2])

vx_new = np.zeros((len(vx), 1))
vy_new = np.zeros((len(vy), 1))

for i in range(len(vx)-1):
    vx_new[i+1] = cos(yaw_pose[i]) * vx[i+1] + sin(yaw_pose[i]) * vy[i+1]
    vy_new[i+1] = sin(yaw_pose[i]) * (-1)* vx[i+1] +  cos(yaw_pose[i])* vy[i+1]


f_plot(t_pose, vx_new, colors=colors, linewidth=2.)
f_plot(t_pose, vy_new, colors=colors, linewidth=2.)
f_plot(t_pose, dx, colors=colors, linewidth=2.)
f_plot(t_pose, dy, colors=colors, linewidth=2.)

'''
f_plot(t_pose, x_pose, colors=colors, linewidth=2.)
f_plot(t_pose, y_pose, colors=colors, linewidth=2.)
f_plot(t_pose, ddx, colors=colors, linewidth=2.)
f_plot(t_pose, ddy, colors=colors, linewidth=2.)
f_plot(x_pose, y_pose, colors=colors, linewidth=2.)
'''
plt.show()

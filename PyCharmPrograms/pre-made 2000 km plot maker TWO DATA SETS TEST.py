import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
import pandas as pd
from optparse import OptionParser
import readnc
import sys
import time
import array as arr
import matplotlib.axes as ax
import MandNsubs as sub
from netCDF4 import Dataset
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib
start_time = time.time()
#creates values for plotting axis of 2000 km plot
lat_coord_array = np.zeros(200, dtype=float) #initiates latitude values
long_coord_array = np.zeros(200, dtype=float) #initiates longitude values
coordinate_row = -45.3 #top left corner lat value
coordinate_col = 307.5 #top left corner long value
lat_resolution = 10/111.111
long_resolution = (10 / (111.111 * np.cos(np.deg2rad(54.3))))
plt_array = np.zeros((200,200), dtype= 'float')
for r in range (0,200):
    for c in range(0,200):
        lat_coord_array[r] = coordinate_row
        long_coord_array[c] = coordinate_col
        coordinate_col += long_resolution
    coordinate_row -= lat_resolution
    coordinate_col = 307.5

data_file1 = '/Volumes/Blanken_HD/8_10_and_300_30_QuikSCAT_CONFIRMED.txt' #DATA FILE 1 MUST BE A QUIKSCAT TEXT FILE SO THAT THE MASKING WORKS CORRECTLY
read_data_file1 = open(data_file1, 'r+')
all_lines1 = read_data_file1.readlines()
data_file2 = '/Volumes/Blanken_HD/8_10_and_300_30_ERA_5_data_CONFIRMED.txt'
read_data_file2 = open(data_file2, 'r+')
all_lines2 = read_data_file2.readlines()
ERA_5_array = np.zeros((200,200), dtype = 'float')
QuikSCAT_array = np.zeros((200,200), dtype = 'float')
for l in range(0,len(all_lines1)):
    currentLine1 = all_lines1[l]
    currentLine2 = all_lines2[l]
    r_value = int(currentLine1[0:3])
    c_value = int(currentLine1[4:7])
    wind_speed1 = float(currentLine1[8:18])
    wind_speed2 = float(currentLine2[8:18])
    if np.isnan(wind_speed1) == True:
        wind_speed1 = QuikSCAT_array[r_value,c_value-1]
    QuikSCAT_array[r_value,c_value] = wind_speed1
    if wind_speed1 == 0: #checks for land masses
        ERA_5_array[r_value, c_value] = 100

    ERA_5_array[r_value,c_value] = wind_speed2

ERA_5_array = np.flipud(ERA_5_array)
plt_array = ERA_5_array - QuikSCAT_array

print("time: " + str(time.time()-start_time))
TNRfont = {'fontname':'Times New Roman'}
plot = plt.figure(figsize = (6.8,5.3), dpi=100)
plot_variable = plt.imshow(plt_array, extent = [long_coord_array[0], long_coord_array[199],lat_coord_array[199],lat_coord_array[0]], origin='upper',  cmap = 'gnuplot2', aspect= 1.5, vmin = -2, vmax = 2)
plt.ylabel('latitude($^\circ$)', fontsize = 16, **TNRfont)
plt.xlabel('longitude($^\circ$)', fontsize = 16, **TNRfont)
plt.title(('Difference Data' + '\n' + '8-10 m/s and 300-30 degrees'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
cbar = plt.colorbar(plot_variable, fraction=0.05, pad=0.04)
cbarLabel = cbar.set_label('Wind Speed Difference (ERA-5 minus QuikSCAT) (m/s)', fontsize = 16, **TNRfont)
plt.tick_params(axis='both', labelsize=16)
cbar.ax.tick_params(axis='y', labelsize=16)
#plt.savefig('Difference_8_10_and_0_30.svg', dpi=100)
bbox_props = dict(boxstyle="rarrow", fc=(1, 1, 1), ec="r", lw=0)
t = plt.text(332,-48, "0 degrees", ha="center", va="center", rotation=0,size=15,bbox=bbox_props)
bb = t.get_bbox_patch()
bb.set_boxstyle("rarrow", pad=0.6)
plt.show()
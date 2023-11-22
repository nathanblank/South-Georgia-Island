import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
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

plt_array = np.zeros((200,200), dtype= 'float')


data_file = '/Volumes/Blanken_HD/8_10_and_300_30_QuikSCAT_CONFIRMED.txt'
QuikSCAT = True #used to determine whether to flip the data set of not
read_data_file = open(data_file, 'r+')
all_lines = read_data_file.readlines()
coord_counter = 0
sum_wind_speed = 0
for l in range(0,len(all_lines)):
    currentLine = all_lines[l]
    r_value = int(currentLine[0:3])
    c_value = int(currentLine[4:7])
    wind_speed = float(currentLine[8:18])
    print(r_value,c_value,wind_speed)
    plt_array[r_value, c_value] = wind_speed
    if wind_speed > 0:
        sum_wind_speed += wind_speed
        coord_counter += 1

avg_wind_speed = sum_wind_speed / float(coord_counter)
print('Average Wind Speed: ' + str(avg_wind_speed))
print("time: " + str(time.time()-start_time))
TNRfont = {'fontname':'Times New Roman'}
plot = plt.figure(figsize = (6.8,5.3), dpi=100)

if QuikSCAT == True:
    # ETOPO5 mask
    completeName = ('/Volumes/Blanken_HD/ERA5_Output_Data/SGI_and_falklands_in_ETOPO5.txt')
    SGI_in_ETOPO5 = open(completeName, "r")
    all_lines = SGI_in_ETOPO5.readlines()
    currentLine = all_lines[0]
    row_coord = currentLine[0:8]
    col_coord = currentLine[9:17]
    for l in range(0, len(all_lines)):
        currentLine = all_lines[l]
        row_coord = currentLine[0:8]
        # print("test")
        col_coord = currentLine[9:17]
        #print("row coord: " + str(row_coord))
        #print("column coord: " + str(col_coord))
        row_index, col_index = sub.Two_thousand_km_index_finder_from_ETOPO5(row_coord, col_coord)
        plt_array[row_index - 1:row_index + 2, col_index - 1:col_index + 2] = 0
        for r in range(0, 200):
            for c in range(0, 200):
                if plt_array[r,c] == 0:
                    plt_array[r,c] = 100 #easily shows land
                if np.isnan(plt_array[r,c]) == True:
                    plt_array[r,c] = plt_array[r,c-1]

    plt.title(('QuikSCAT Data' + '\n' + '8-10 m/s and 300-30 degrees'), fontdict=None, loc='center', pad=None, fontsize=32, **TNRfont)
else:
    # ETOPO5 mask
    completeName = ('/Volumes/Blanken_HD/ERA5_Output_Data/SGI_and_falklands_in_ETOPO5.txt')
    SGI_in_ETOPO5 = open(completeName, "r")
    all_lines = SGI_in_ETOPO5.readlines()
    currentLine = all_lines[0]
    row_coord = currentLine[0:8]
    col_coord = currentLine[9:17]
    for l in range(0, len(all_lines)):
        currentLine = all_lines[l]
        row_coord = currentLine[0:8]
        # print("test")
        col_coord = currentLine[9:17]
        print("row coord: " + str(row_coord))
        print("column coord: " + str(col_coord))
        row_index, col_index = sub.Two_thousand_km_index_finder_from_ETOPO5(row_coord, col_coord)
        row_index = 200 - row_index  # accounts for flip in ERA-5 data
        plt_array[row_index - 1:row_index + 2, col_index - 1:col_index + 2] = 0
        for r in range(0, 200):
            for c in range(0, 200):
                if plt_array[r,c] == 0:
                    plt_array[r,c] = 100 #easily shows land


    plot_variable = plt.imshow(np.flipud(plt_array), origin='upper', cmap='gnuplot2', aspect=1, vmin=8,vmax=12)

    plt.title(('ERA-5 Data' + '\n' + '8-10 m/s and 300-30 degrees'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)

plt.ylabel('element number', fontsize = 16, **TNRfont)
plt.xlabel('element number', fontsize = 16, **TNRfont)

#corner acc determiner
xstart = 103
xend = 133
ystart = 103
yend = 133
all_map_speed = 0
all_map_element_counter = 0
corner_acc_speed = 0
corner_acc_element_counter = 0
for r in range(0,200):
    for c in range(0,90):
        if plt_array[r, c] != 100 and np.isnan(plt_array[r, c]) != True:
            all_map_speed += plt_array[r,c]
            all_map_element_counter += 1 #makes white box around outside of sampling area
        if c == 89 or r == 0 or c == 0 or r == 199:
            plt_array[r,c] = 100

all_map_speed /= (all_map_element_counter)
print('Average map speed = ' + str(all_map_speed))
for r in range(ystart,yend): #corner acceleration determiner
    for c in range(xstart,xend):
        if plt_array[r,c] >= (all_map_speed) and plt_array[r,c] < 50:
            corner_acc_speed += plt_array[r,c]
            corner_acc_element_counter += 1
            plt_array[r,c] = 10


corner_acc_speed /= corner_acc_element_counter
print('Number of corner acceleration elements = ' +str(corner_acc_element_counter))
print('Corner acceleration speed = ' + str(corner_acc_speed))

plot_variable = plt.imshow(plt_array, origin='upper',  cmap = 'gnuplot2', aspect= 1, vmin = 8, vmax = 12)

cbar = plt.colorbar(plot_variable, fraction=0.05, pad=0.04)
cbarLabel = cbar.set_label('Wind speed (m/s)', fontsize = 16, **TNRfont)
plt.tick_params(axis='both', labelsize=16)
#cbar.ax.tick_params(axis='y', labelsize=16)
plt.savefig('ERA_5_Averaged_8_10_300_30.svg', dpi=100)
plt.show()
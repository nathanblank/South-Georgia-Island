#This program is the main program that will make the 2000 km plots once the text file is already made, hence "pre-made".
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
from matplotlib.colors import LogNorm
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
        #lat_coord_array[r] = coordinate_row
        #long_coord_array[c] = coordinate_col
        #coordinate_col += long_resolution
    #coordinate_row -= lat_resolution
    #coordinate_col = 307.5
        lat_coord_array[r] = 1000 - (r*10)
        long_coord_array[c] = (c*10) - 1000

data_file = '/Volumes/Blanken_HD/South Georgia Project/8_10_and_300_30_QuikSCAT_NEW_MASTER.txt'
QuikSCAT = True #used to determine whether to flip the data set of not. Set true if the data file above is QuikSCAT, set false if ERA-5
read_data_file = open(data_file, 'r+')
all_lines = read_data_file.readlines()
coord_counter = 0
sum_wind_speed = 0
min_speed = 100
for l in range(0,len(all_lines)):
    currentLine = all_lines[l]
    r_value = int(currentLine[0:3])
    c_value = int(currentLine[4:7])
    wind_speed = float(currentLine[8:18])
    print(r_value,c_value,wind_speed)
    #Conditional
    #if 52 <= r_value < 143:
      #  if 81 <= c_value < 181:
        #    plt_array[r_value, c_value] = wind_speed
    #Single Swath
    plt_array[r_value, c_value] = wind_speed
    if wind_speed > 0:
        sum_wind_speed += wind_speed
        coord_counter += 1


avg_wind_speed = sum_wind_speed / float(coord_counter)
print('Average Wind Speed: ' + str(avg_wind_speed))
print("time: " + str(time.time()-start_time))
for r in range(60,110):
    for c in range(100,150):
        if plt_array[r,c] < min_speed and plt_array[r,c] != 0.0:
            min_speed = plt_array[r,c]
            print(r, c, "Min speed: " + str(min_speed))
print("Min speed: " + str(min_speed))
TNRfont = {'fontname':'Times New Roman'}
plot = plt.figure(figsize = (6.8,5.3), dpi=100)

if QuikSCAT == True:
    avg_speed_tracker = np.mean(plt_array[0:200, 0:90])

    # ETOPO5 mask
    completeName = ('/Volumes/Blanken_HD/South Georgia Project/ERA5_Output_Data/SGI_and_falklands_in_ETOPO5.txt')
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

    # QuikSCAT islands

    ISLANDcompleteName = ('/Volumes/Blanken_HD/South Georgia Project/QuikSCAT islands.txt')
    QuikSCAT_islands = open(ISLANDcompleteName, "r")
    all_ISLAND_lines = QuikSCAT_islands.readlines()
    for l in range(0, len(all_ISLAND_lines)):
        currentISLANDLine = all_ISLAND_lines[l]
        r_value = int(currentISLANDLine[0:3])
        c_value = int(currentISLANDLine[4:7])
        print(r_value, c_value)
        plt_array[r_value, c_value] = 100

    #print('Average Wind Speed: ' + str(9.454))
    #print("Average upwind speed * .9: " + str(.9 * 9.454))
    #for r in range(0, 200):
     #   for c in range(0, 200):
      #      if plt_array[r, c] <= (.9 * avg_speed_tracker):
      #          plt_array[r, c] = 10

    #full 2000 km plot
    #plot_variable = plt.imshow(plt_array,origin='upper', extent = [long_coord_array[0], long_coord_array[199], lat_coord_array[199],lat_coord_array[0]], cmap = 'gnuplot2', vmin = 8.5, vmax =11.5)
    #plt.plot([-100, -100, -600, -600, -100], [100, -100, -100, 100, 100], 'r-', linewidth=3)

    # up close
    plot_variable = plt.imshow(plt_array[52:143,81:181], origin='upper',extent=[long_coord_array[81], long_coord_array[181], lat_coord_array[142],lat_coord_array[52]], cmap='gnuplot2', aspect=1, vmin=8.5, vmax=11.5)

    #Wind shadow box (400 km long, 500 km lat)
    #plt.plot([100, 100, 500, 500, 100], [-100, 400, 400, -100, -100], 'r-', linewidth=3)

    # bottom corner acc determiner
    #plt.plot([30, 30, 330, 330, 30], [-30, -330, -330, -30, -30], 'r-', linewidth=3)

    # top corner acc determiner
    #plt.plot([30, 30, 150, 150, 30], [180, 20, 20, 180, 180], 'r-', linewidth=3)

    plt.title(('Single QuikSCAT Rev' + '\n' + 'from Feb 12, 2005'), fontdict=None, loc='center', pad=None, fontsize=32, **TNRfont)


else: #For any data files that are ERA-5
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
    # QuikSCAT islands
    plt_array = np.flipud(plt_array)
    ISLANDcompleteName = ('/Volumes/Blanken_HD/QuikSCAT islands.txt')
    QuikSCAT_islands = open(ISLANDcompleteName, "r")
    all_ISLAND_lines = QuikSCAT_islands.readlines()
    for l in range(0, len(all_ISLAND_lines)):
        currentISLANDLine = all_ISLAND_lines[l]
        r_value = int(currentISLANDLine[0:3])
        c_value = int(currentISLANDLine[4:7])
        print(r_value,c_value)
        plt_array[r_value, c_value] = 100
    #conditional mean full 2000 km
    #plot_variable = plt.imshow(plt_array, extent=[long_coord_array[0], long_coord_array[199], lat_coord_array[199],lat_coord_array[0]], origin='upper', cmap='gnuplot2', aspect=1, vmin=0,vmax=20)

    #up close
    plot_variable = plt.imshow(plt_array[52:143, 81:181],extent=[long_coord_array[81], long_coord_array[180], lat_coord_array[142],lat_coord_array[52]], origin='upper', cmap='gnuplot2', aspect=1, vmin=0,vmax=20)

    #single swath
    #plot_variable = plt.imshow(plt_array, extent=[long_coord_array[0], long_coord_array[199], lat_coord_array[199],lat_coord_array[0]], origin='upper', cmap='gnuplot2', aspect=1, vmin=8.5,vmax=11.5)

    plt.title(('Single ERA-5 Map' + '\n' + 'from Feb 12, 2005'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)

#plt.ylabel('latitude($^\circ$)', fontsize = 16, **TNRfont)
#plt.xlabel('longitude($^\circ$)', fontsize = 16, **TNRfont)

plt.ylabel('Disance from SGI (km)', fontsize = 16, **TNRfont)
plt.xlabel('Distance from SGI (km)', fontsize = 16, **TNRfont)





#Makes arrow on plot
#bbox_props = dict(boxstyle="rarrow", fc=(1, 1, 1), ec="r", lw=0)
#t = plt.text(500,750, "0 degrees", ha="center", va="center", rotation=0,size=15,bbox=bbox_props)
#bb = t.get_bbox_patch()
#bb.set_boxstyle("rarrow", pad=0.6)


cbar = plt.colorbar(plot_variable, fraction=0.05, pad=0.04)
cbarLabel = cbar.set_label('Wind speed (m/s)', fontsize = 16, **TNRfont)
plt.tick_params(axis='both', labelsize=16)
#cbar.ax.tick_params(axis='y', labelsize=16)
plt.savefig('ERA_5_data_Averaged_8_10_300_30.svg', dpi=100)
plt.show()
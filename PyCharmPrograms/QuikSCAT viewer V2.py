#This program makes a plot of a single QuikSCAT rev over the SGI region
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



# time it from here
start_time = time.time()

fline = '/Volumes/Blanken_HD/Satellite_Data/QSCAT_v3_1_download/QS2005/043/qs_l2b_29434_v3.1_200502120915.nc'

ncfile = fline

try:
    nc_file = Dataset( ncfile, 'r' )
    print("file is ok")
except IOError:
    print('not a valid netCDF file')
#print(nc_file)


from datetime import date, timedelta, datetime

[attr_list, global_attr] = readnc.readGlobalAttrs( nc_file )

[vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )





#descending QuikSCAT limits
rowBegin= 2823
rowEnd = 3058
colBegin = 0
colEnd = 152
#ascending QuikSCAT limits
rowBegin= 237
rowEnd = 425
colBegin = 0
colEnd = 152
#testing values
rowBegin= 190
rowEnd = 425
start_time = time.time() #determines starting time

time_Array = var_data_list[0]
lat_Array = var_data_list[1]
long_Array = var_data_list[2]
windSpeed_Array = var_data_list[3]
windDirection_Array = var_data_list[4]
rain_Array = var_data_list[5]
flags_Array = var_data_list[6]

lat_resolution = 10/111.111
long_resolution = (10 / (111.111 * np.cos(np.deg2rad(54.3))))


plt_array = np.zeros((200,200), dtype=float) #initiates plot array
lat_coord_array = np.zeros(200, dtype=float) #initiates latitude values
long_coord_array = np.zeros(200, dtype=float) #initiates longitude values

coordinate_row = -45.3 #top left corner lat value
coordinate_col = 307.5 #top left corner long value
counter = 0

for r in range (0,200):
    for c in range(0,200):
        lat_coord_array[r] = coordinate_row
        long_coord_array[c] = coordinate_col
        coordinate_col += long_resolution
    coordinate_row -= lat_resolution
    coordinate_col = 307.5

for r in range (rowBegin,rowEnd):
    for c in range(colBegin,colEnd):
        if long_Array[r,c] < 338.3:
            if long_Array[r,c] > 307.5:
                if lat_Array[r,c] < -45.3:
                    if lat_Array[r,c] > -63.3:
                       if 0 == 0:
                            print('r: ' + str(r) + ', c: ' + str(c))
                            row_index, col_index = sub.Two_thousand_km_index_finder(lat_Array[r,c],long_Array[r,c])
                            print("original row: " + str(row_index) + ', original col: ' + str(col_index))
                            if row_index < 0:
                                row_index += 199
                            if col_index < 0:
                                col_index += 199
                            print("updated row: " + str(row_index) + ', updated col: ' + str(col_index))
                            print("Coordinate: (" + str(sub.truncate(lat_Array[r, c], 4)) + ", " + str(sub.truncate(long_Array[r, c], 4)) + ") is index: (" + str(row_index) + ", " + str(col_index) + ")")
                            print('Rain flag value: ' + str(rain_Array[r,c]))
                            print('Quality of data: ' + str(flags_Array[r,c]))
                            print('Wind speed: ' + str(windSpeed_Array[r,c]))
                            try:
                                plt_array[row_index, col_index] = windSpeed_Array[r, c]
                            except:
                                print("Out of range")
                            print()
                            print()
                            print(long_resolution)


for r in range (0,200):
    for c in range(0,200):
        if np.isnan(plt_array[r,c]) == True:
            plt_array[r,c] = 100

output_file = '/Volumes/Blanken_HD/feb_12_2005_QuikSCAT.txt'
read_output_file = open(output_file, 'w+')


for r in range(0, 200):
    for c in range(0, 200):
        read_output_file.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array[r,c]) + '\n') #writes out [0:3] of row value, [4:7] col value and a guaranteed [8:16] of the wind speed


        print(r,c, plt_array[r,c])
read_output_file.close()
TNRfont = {'fontname':'Times New Roman'}
plot = plt.figure(figsize = (6.8,5.3), dpi=100)
plot_variable = plt.imshow(plt_array,  origin='upper',  cmap = 'gnuplot2', aspect= 1, vmax = 20)
#extent = [long_coord_array[0], long_coord_array[199],lat_coord_array[199],lat_coord_array[0]],
plt.ylabel('latitude($^\circ$)', fontsize = 16, **TNRfont)
plt.xlabel('longitude($^\circ$)', fontsize = 16, **TNRfont)
plt.title(('QuikSCAT Swath Showing' + '\n' + ' Wind Shadow'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
cbar = plt.colorbar(plot_variable, fraction=0.05, pad=0.04)
cbarLabel = cbar.set_label('Wind speed (m/s)', fontsize = 16, **TNRfont)
plt.tick_params(axis='both', labelsize=16)
cbar.ax.tick_params(axis='y', labelsize=16)
plt.savefig('QuikSCAT.svg', dpi=100)
plt.show()


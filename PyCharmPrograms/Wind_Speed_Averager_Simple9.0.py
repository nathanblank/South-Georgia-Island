#This program takes in a month of ERA-5 maps and then can average any range of maps within that range
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from optparse import OptionParser
import readnc
import sys
import time
import MandNsubs as sub
import array as arr
import matplotlib.axes as ax

from netCDF4 import Dataset
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib

#  A prog to investigate the structure of the ERA5 u10/v10 files downloaded from Copernicus
# based on netcdf read code from census_8a.py





# time it from here
start_time = time.time()

#fline = '/Volumes/Satellite_Data/ERA5_downloads/2001_01_uv.nc'     # This is a sample absolute address
fline = '/Volumes/Blanken_HD/ERA5_Data/ERA5_downloads/2000_01_uv.nc'


ncfile = fline

try:
    nc_file = Dataset( ncfile, 'r' )
    print("file is ok")
except IOError:
    print('not a valid netCDF file')
print(nc_file)

completeName = ('/Volumes/Blanken_HD/ERA5_Output_Data/SGI_in_ETOPO5.txt')
SGI_in_ETOPO5 = open(completeName, "r")

#Date and time for plot
import datetime
from datetime import date, timedelta, datetime

[attr_list, global_attr] = readnc.readGlobalAttrs( nc_file )
#need to convert time/date input into map numbers

mapNumBegin = 15 #mapNumBegin is the map number you're looking at
mapNumEnd = 15 # last map number
mapNum = 0
[vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )
u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
w10 = var_data_list[2]  # time for each data map
#creates values for plotting axis of 2000 km plot
lat_coord_array = np.zeros(200, dtype=float) #initiates latitude values
long_coord_array = np.zeros(200, dtype=float) #initiates longitude values
coordinate_row = -45.3 #top left corner lat value
coordinate_col = 307.5 #top left corner long value
lat_resolution = 10/111.111
long_resolution = (10 / (111.111 * np.cos(np.deg2rad(54.3))))
plt_array = np.zeros((200,200), dtype = 'float')
for r in range (0,200):
    for c in range(0,200):
        lat_coord_array[r] = coordinate_row
        long_coord_array[c] = coordinate_col
        coordinate_col += long_resolution
    coordinate_row -= lat_resolution
    coordinate_col = 307.5

#ERA-5 plot limits
rowBegin= 523
rowEnd = 610
colBegin = 1198
colEnd = 1378
#2000 km plot limits
rowBegin= 541
rowEnd = 613
colBegin = 1230
colEnd = 1353

#World map limits
#rowBegin= 0
#rowEnd = 720
#colBegin = 0
#colEnd = 1439
start_time = time.time() #determines starting time
ERA5_characteristics= open("ERA5_properties.txt","w+")
ERA5_characteristics.write('File name' + fline + '\r\n')

#from here down are goal numbers 2 and 3, plot the data within the ERA5 box
w10_pltBegin = w10[mapNumBegin] #used to determine beginning time
w10_pltEnd = w10[mapNumEnd] # used to determine end time

u10_plt = u10[mapNumBegin, :,:]  # defines u10_plt
v10_plt = v10[mapNumBegin, :,:] # defines v10_plt
mapNumLoopVar = 0 #will be used to count how many coordinate points are being looked at.
dirmean = 0
for h in range(mapNumBegin, mapNumEnd+1):

    map_spd = np.sqrt(u10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2) #determines map speed over all of the maps that it looks through
    print('Map num: ' + str(h))
    print('Map speed: ' + str(np.mean(map_spd)))
    ERA5_characteristics.write(str(h) + ', '+ str(np.mean(map_spd)) + '\r\n')
    #ERA5_characteristics.write(str(np.mean(map_spd)) + '\r\n')
    u10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += u10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
    v10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += v10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
    umean = np.mean(u10[h, rowBegin:rowEnd + 1, colBegin:colEnd + 1])
    vmean = np.mean(v10[h, rowBegin:rowEnd + 1, colBegin:colEnd + 1])
    map_dir = np.rad2deg(np.arctan2(vmean, umean))  # vector mean calculation in degrees
    if map_dir < 0:
        map_dir = map_dir + 360
    print('Map direction: ' + str(map_dir))
    u10_plt = u10_plt / (mapNumEnd - (mapNumBegin-1))
    v10_plt = v10_plt / (mapNumEnd - (mapNumBegin-1))
    dirmean += map_dir
dirmean = dirmean / ((mapNumEnd-mapNumBegin)+1)
ERA5_characteristics.close()
print(map_spd.shape)
atmp = map_spd
tmp_mean = np.mean(atmp)


# note that var_data_list[2] is a 1-D array of MAP TIMES, var_data_list[1] is a 1-D array of LATITUDES for each map,
#         and var_data_list[0] is a 1-D array of LONGITUDES for each map

longArray = var_data_list[0]
latArray = var_data_list[1]
print()
print()
print("Average wind speed is: ", tmp_mean, " m/s")

print("Average wind direction is: ", dirmean, " degrees")

completeName = ('/Volumes/Blanken_HD/ERA5_Output_Data/SGI_in_ETOPO5.txt')
SGI_in_ETOPO5 = open(completeName, "r")
all_lines = SGI_in_ETOPO5.readlines()
currentLine = all_lines[0]
row_coord = currentLine[0:8]
col_coord = currentLine[9:17]
for l in range (0, len(all_lines)):
    currentLine = all_lines[l]
    row_coord = currentLine[0:8]
    #print("test")
    col_coord = currentLine[9:17]
    print("row coord: " + str(row_coord))
    print("column coord: " + str(col_coord))
    row_index, col_index = sub.ERA5_index_finder_QuikSCAT_region(row_coord, col_coord)
    atmp[row_index,col_index] = 100
# determines beginning time for output
daysChange = w10_pltBegin / 24

newDTBegin = timedelta(np.float64(w10_pltBegin / 24.))
dtBegin = datetime(1900, 1, 1) + newDTBegin

print()

# determines end time for output
daysChange = w10_pltEnd / 24
print(daysChange)
newDTEnd = timedelta(np.float64(w10_pltEnd / 24.))
dtEnd = datetime(1900, 1, 1) + newDTEnd
aatmp = np.flipud(atmp)
fig = plt.figure()
print(fig)

for r in range(rowBegin,rowEnd+1):
    for c in range(colBegin,colEnd+1):
        row_index, col_index = sub.Two_thousand_km_index_finder(latArray[r],longArray[c])
        plt_array[row_index,col_index] = aatmp[r,c]
TNRfont = {'fontname':'Times New Roman'}
plot = plt.figure(figsize = (6.1,5.4), dpi=100)
plot_variable = plt.imshow(plt_array, extent = [long_coord_array[0],long_coord_array[199],lat_coord_array[199],lat_coord_array[0]], origin='lower', aspect= 1.5, vmin = 0, vmax = 20, cmap = 'gnuplot2')
plt.ylabel('latitude($^\circ$)', fontsize = 16, **TNRfont)
plt.xlabel('longitude($^\circ$)', fontsize = 16, **TNRfont)
#plt.title(('Average Wind Speeds From ' + str(dtBegin) +' to '+ str(dtEnd) + ' in m/s'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
plt.title(('Average Wind Speeds On ' + '\n' + str(dtBegin)), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
cbar = plt.colorbar(plot_variable, fraction=0.05, pad=0.04)
cbarLabel = cbar.set_label('Wind speed (m/s)', fontsize = 16, **TNRfont)
plt.tick_params(axis='both', labelsize=16)
cbar.ax.tick_params(axis='y', labelsize=16)
plt.savefig('ERA_5.svg', dpi=100)
plt.show()
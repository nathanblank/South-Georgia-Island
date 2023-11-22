#This program just plots any ERA-5 map over the SGI 2000 km region
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from optparse import OptionParser
import readnc
import sys
import time
import array as arr


from netCDF4 import Dataset
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt

#  A prog to investigate the structure of the ERA5 u10/v10 files downloaded from Copernicus
# based on netcdf read code from census_8a.py





# time it from here
start_time = time.time()

fline = '/Volumes/Blanken_HD/ERA5_Data/ERA5_downloads/2000_02_uv.nc'     # This is a sample absolute address
#fline = '/Users/N-Dogg/Downloads/SRT IV/ECMWF_ERA5_Analyses/2001_02_uv.nc'
# now read the ERA5 file and close it
ncfile = fline

try:
    nc_file = Dataset( ncfile, 'r' )
    print("file is ok")
except IOError:
    print('not a valid netCDF file')
#creates values for plotting axis of 2000 km plot
lat_coord_array = np.zeros(200, dtype=float) #initiates latitude values
long_coord_array = np.zeros(200, dtype=float) #initiates longitude values
coordinate_row = -45.3 #top left corner lat value
coordinate_col = 307.5 #top left corner long value
lat_resolution = 10/111.111
long_resolution = (10 / (111.111 * np.cos(np.deg2rad(54.3))))
for r in range (0,200):
    for c in range(0,200):
        lat_coord_array[r] = coordinate_row
        long_coord_array[c] = coordinate_col
        coordinate_col += long_resolution
    coordinate_row -= lat_resolution
    coordinate_col = 307.5


[attr_list, global_attr] = readnc.readGlobalAttrs( nc_file )
#need to convert time/date input into map numbers
mapNumBegin = 90 #mapNumBegin is the map number you're looking at
mapNumEnd = mapNumBegin - 1 # for outputting one map, type the value of mapNumBegin - 1
mapNum = mapNumBegin
[vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )
u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
w10 = var_data_list[2]  # time for each data map

u10_avg = 0
v10_avg = 0
#plt.axis([1198.4, 1377.2, 523.4, 609.6])
#ERA-5 plot limits
rowBegin= 523
rowEnd = 610
colBegin = 1198
colEnd = 1378
#2000 km plot limits
#row_middle = 578
#col_middle = 1291
#rowBegin= 540
#rowEnd = 614
#colBegin = 1230
#colEnd = 1353

#200 km lat x 500 km long west of island
rowBegin= 574
rowEnd = 582
colBegin = 1255
colEnd = 1285

#rowBegin= 523
#rowEnd = 525
#colBegin = 1198
#colEnd = 1200
vertAdder = 0.
horizAdder = 0.

start_time = time.time()

#
#from here down are goal numbers 2 and 3, plot the data within the ERA5 box
w10_pltBegin = w10[mapNumBegin] #used to determine beginning time
w10_pltEnd = w10[mapNumEnd+1] # used to determine end time
w10_plt = w10[mapNum]
print(w10_plt)
u10_plt = u10[mapNum,:,:]  # defines u10_plt
v10_plt = v10[mapNum,:,:] # defines v10_plt
spd_plt = np.sqrt(u10_plt**2 + v10_plt**2) #sqrt of e-w speed squared + n-s speed squared
atmp = spd_plt[rowBegin:rowEnd, colBegin:colEnd]
print(atmp.shape)

#Date and time for plot
import datetime
from datetime import date, timedelta, datetime

daysChange = w10_pltBegin / 24
print(daysChange)
newDTBegin = timedelta(np.float64(w10_pltBegin / 24.))
dtBegin = datetime(1900, 1, 1) + newDTBegin
print(newDTBegin)
print('Date of map begins at',dtBegin)
print(w10_pltBegin, ' begin hours after Jan 1, 1900 is:',dtBegin)


#Calculate mean speed in box
mean = 0.
for i in range(colBegin, colEnd):
    for j in range(rowBegin, rowEnd):
        mean += spd_plt[j,i]
mean = mean /((colEnd - colBegin) * (rowEnd - rowBegin))
atmp = spd_plt[rowBegin:rowEnd, colBegin:colEnd]
tmp_mean = np.mean(atmp)

# note that var_data_list[2] is a 1-D array of MAP TIMES, var_data_list[1] is a 1-D array of LATITUDES for each map,
#         and var_data_list[0] is a 1-D array of LONGITUDES for each map

longArray = var_data_list[0]
latArray = var_data_list[1]
print()
print()
print(mean, tmp_mean)
print("Average wind speed is: ", tmp_mean, " m/s")
#print("Upwind speed: " + str(np.mean(atmp[rowBegin:rowEnd, colBegin:1285])))
#plt.matshow(atmp, cmap='jet')
aatmp = np.flipud(atmp)
#aatmp = np.fliplr(aatmp)
plt.imshow(aatmp, extent = [long_coord_array[40], long_coord_array[90], lat_coord_array[110], lat_coord_array[90]], cmap = 'gnuplot2', origin='lower', aspect= 2.0)

#plt.contour(aatmp, origin = 'lower',extent = [longArray[colEnd], longArray[colBegin], latArray[rowEnd], latArray[rowBegin]], linewidths = 1) #makes resolution more "flowy" and not "pixely"
#Y, X = np.mgrid[0:4320:100j, 0:2160:100j]
#plt.streamplot(X, Y, u10_plt, v10_plt) #shows arrows, might be good for speed and direction
#x = longitude
#y = latitude
plt.title((dtBegin), fontdict=None, loc='center', pad=None)
#plt.axis([-60,-40, 360, 300])
plt.colorbar() #shows wind speed bar from blue to red
plt.show()
plt.savefig(fname = 'ERA5map.png')
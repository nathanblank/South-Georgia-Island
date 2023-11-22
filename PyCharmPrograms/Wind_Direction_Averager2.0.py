#This program plots the average direction at each element over the SGI region based on a specified range of ERA-5 maps
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

from netCDF4 import Dataset
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib

#  A prog to investigate the structure of the ERA5 u10/v10 files downloaded from Copernicus
# based on netcdf read code from census_8a.py





# time it from here
start_time = time.time()

#fline = '/Volumes/Satellite_Data/ERA5_downloads/2001_01_uv.nc'     # This is a sample absolute address
fline = '/Volumes/Blanken_HD/ERA5_data/ERA5_downloads/2001_01_uv.nc'
# now read the ERA5 file and close it
ncfile = fline

try:
    nc_file = Dataset( ncfile, 'r' )
    print("file is ok")
except IOError:
    print('not a valid netCDF file')


[attr_list, global_attr] = readnc.readGlobalAttrs( nc_file )
#need to convert time/date input into map numbers
mapNumBegin = 0 #mapNumBegin is the map number you're looking at
mapNumEnd = 0 # last map number
mapNum = 0
[vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )
u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
w10 = var_data_list[2]  # time for each data map

u10_avg = 0
v10_avg = 0
#plt.axis([1198.4, 1377.2, 523.4, 609.6])
#Outputs entire world
rowBegin= 0
rowEnd = 720
colBegin = 0
colEnd = 1439
#ERA-5 plot limits
rowBegin= 523
rowEnd = 610
colBegin = 1198
colEnd = 1378


start_time = time.time()

#
#from here down are goal numbers 2 and 3, plot the data within the ERA5 box
w10_pltBegin = w10[mapNumBegin] #used to determine beginning time
w10_pltEnd = w10[mapNumEnd] # used to determine end time
w10_plt = w10[mapNum]
print(w10_plt)
u10_plt = u10[mapNumBegin, :,:]  # defines u10_plt
v10_plt = v10[mapNumBegin, :,:] # defines v10_plt


for h in range(mapNumBegin, mapNumEnd+1):
    u10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += u10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
    v10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += v10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
    u10_plt = u10_plt / (mapNumEnd - (mapNumBegin-1))
    v10_plt = v10_plt / (mapNumEnd - (mapNumBegin-1))
    print('Map num: ' + str(h))

drt_plt = np.rad2deg(np.arctan2(v10_plt[:,:],u10_plt[:,:]))
atmp = drt_plt[rowBegin:rowEnd, colBegin:colEnd]
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

print()

daysChange = w10_pltEnd / 24
print(daysChange)
newDTEnd = timedelta(np.float64(w10_pltEnd / 24.))
dtEnd = datetime(1900, 1, 1) + newDTEnd
print(newDTEnd)
print('Date of map ends at',dtEnd)
print(w10_pltEnd, ' end hours after Jan 1, 1900 is:',dtEnd)


#Calculate mean direction in ERA-5 box
umean = 0.
vmean = 0.

umean = np.mean(u10_plt[rowBegin:rowEnd+1,colBegin:colEnd+1])
vmean = np.mean(v10_plt[rowBegin:rowEnd+1,colBegin:colEnd+1])
dirmean = np.rad2deg(np.arctan2(vmean,umean))  #vector mean calculation


# note that var_data_list[2] is a 1-D array of MAP TIMES, var_data_list[1] is a 1-D array of LATITUDES for each map,
#         and var_data_list[0] is a 1-D array of LONGITUDES for each map

longArray = var_data_list[0]
latArray = var_data_list[1]
print()
print()
print('Average wind direction is: ' + str(dirmean) + ' degrees from east')
#plt.matshow(atmp, cmap='jet'
aatmp = np.flipud(atmp)
#aatmp = np.fliplr(aatmp)
fig = plt.figure()

#ax1 = fig.add_subplot(211)
#ax1.set_ylabel('longitude(degrees)')
#ax1.set_xlabel('latitude(degrees)')
plt.xlabel('latitude($^\circ$)')
plt.ylabel('longitude($^\circ$)')
plt.imshow(aatmp, extent = [longArray[colBegin], longArray[colEnd], latArray[rowEnd], latArray[rowBegin]], origin='lower', aspect= 1.0)


#plt.contour(aatmp, origin = 'lower',extent = [longArray[colEnd], longArray[colBegin], latArray[rowEnd], latArray[rowBegin]], linewidths = 1) #makes resolution more "flowy" and not "pixely"
#Y, X = np.mgrid[0:4320:100j, 0:2160:100j]
#plt.streamplot(X, Y, u10_plt, v10_plt) #shows arrows, might be good for speed and direction
#x = longitude
#y = latitude

plt.title(('Average Wind Directions From ' + str(dtBegin) + ' to ' + str(dtEnd)), fontdict=None, loc='center', pad=None)
cbar = plt.set_cmap('hsv') #shows cyclical wind direction bar
cbar = plt.colorbar()
cbarLabel = cbar.set_label('Wind direction ($^\circ$) (0$^\circ$ is east)')

plt.show()
plt.savefig(fname = 'ERA5map.png')
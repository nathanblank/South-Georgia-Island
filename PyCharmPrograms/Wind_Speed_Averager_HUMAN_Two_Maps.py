#This program allows the user to put in two separate dates and times, selects those maps, and then creates an average plot from them.
#Both times must be in the range of the input file
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





# time it from here
start_time = time.time()

#fline = '/Volumes/Satellite_Data/ERA5_downloads/2001_01_uv.nc'     # This is a sample absolute address
fline = '/Users/N-Dogg/Downloads/SRT IV/ECMWF_ERA5_Analyses/2001_01_uv.nc'
#fline = '/Users/N-Dogg/Downloads/SRT IV/ECMWF_ERA5_Analyses/2001_0' + str(m) + '_uv.nc'
# now read the ERA5 file and close it
ncfile = fline

try:
    nc_file = Dataset( ncfile, 'r' )
    print("file is ok")
except IOError:
    print('not a valid netCDF file')



#Date and time for plot
import datetime
from datetime import date, timedelta, datetime
mapNum = 0
[vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )
u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
w10 = var_data_list[2]  # time for each data map

def ERA5MapNumberDeterminer(human_year,human_month,human_day,human_hour,min,sec):

    mapNum = 0


    time_difference = datetime(human_year,human_month,human_day,human_hour,min,sec) - datetime(1900, 1, 1,0,0,0)
    print(time_difference)

    time_difference = time_difference.days #takes the long number and 'days' and pulls out just the number of hours
    hoursSinceTrueStart = (time_difference*24) + human_hour #the datetime did not properly account for hours, so I have to add it here
    print(hoursSinceTrueStart)
    if hoursSinceTrueStart > (len(w10)-1) and hoursSinceTrueStart < w10[0]: #checks that the time input is within the file that is being examined
        print('Map is NOT in range')
    print()

    #this for loop is going to find the array position of the number of hours of time put in
    human_mapNum = 0
    for i in range(0,len(w10)-1):
        print(hoursSinceTrueStart)
        print('Checking: ' + str(w10[i]))
        if hoursSinceTrueStart == w10[i]:
            human_mapNum = i
            print('Map number is: ' + str(human_mapNum))
            break

    return human_mapNum


[attr_list, global_attr] = readnc.readGlobalAttrs( nc_file )
#test cases for dates and times
start_human_year = 2001
start_human_month = 1
start_human_day = 1
start_human_hour = 0
end_human_year = 2001
end_human_month = 1
end_human_day = 10
end_human_hour = 18
min = 0
sec = 0

#allows for real human input
start_human_year = int(input('Input start year: '))
start_human_month = int(input('Input start month: '))
start_human_day = int(input('Input start day: '))
start_human_hour = int(input('Input start hour (interval of 6 and between 0 - 24): '))
end_human_year = int(input('Input end year: '))
end_human_month = int(input('Input end month: '))
end_human_day = int(input('Input end day: '))
end_human_hour = int(input('Input end hour (interval of 6 and between 0 - 24): '))
mapNumBegin = ERA5MapNumberDeterminer(start_human_year,start_human_month,start_human_day,start_human_hour,0,0) #mapNumBegin is the map number you're looking at
mapNumEnd = ERA5MapNumberDeterminer(end_human_year,end_human_month,end_human_day,end_human_hour,0,0) # last map number

#after this point, the code is the same as if the program was averaging all of the maps together between two map numbers


#ERA-5 plot limits
rowBegin= 523
rowEnd = 610
colBegin = 1198
colEnd = 1378

#World map limits
rowBegin= 0
rowEnd = 720
colBegin = 0
colEnd = 1439

start_time = time.time() #determines starting time
ERA5_characteristics= open("ERA5_characteristics.txt","w+")
ERA5_characteristics.write('File name' + fline + '\r\n')

#from here down are goal numbers 2 and 3, plot the data within the ERA5 box

u10_plt = u10[mapNumBegin, :,:]  # defines u10_plt
v10_plt = v10[mapNumBegin, :,:] # defines v10_plt
mapNumLoopVar = 0 #will be used to count how many coordinate points are being looked at.

for h in range(mapNumBegin, mapNumEnd+1):
    map_spd = np.sqrt(u10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2) #determines map speed over all of the maps that it looks through
    print('Map num: ' + str(h))
    print('Map speed: ' + str(np.mean(map_spd)))
    ERA5_characteristics.write(str(h) + ', '+ str(np.mean(map_spd)) + '\r\n')
    #ERA5_characteristics.write(str(np.mean(map_spd)) + '\r\n')
    u10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += u10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
    v10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += v10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
    u10_plt = u10_plt / (mapNumEnd - (mapNumBegin-1))
    v10_plt = v10_plt / (mapNumEnd - (mapNumBegin-1))
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


aatmp = np.flipud(atmp)
fig = plt.figure()


plt.xlabel('latitude($^\circ$)')
plt.ylabel('longitude($^\circ$)')

plt.imshow(aatmp, extent = [longArray[colBegin], longArray[colEnd], latArray[rowEnd], latArray[rowBegin]], origin='lower', aspect= 1.0)

plt.title(('Average Wind Speeds From ' + str(datetime(start_human_year,start_human_month,start_human_day,start_human_hour,min,sec)) +' to '+ str(datetime(end_human_year,end_human_month,end_human_day,end_human_hour,min,sec)) + ' in m/s'), fontdict=None, loc='center', pad=None)

cbar = plt.colorbar() #shows wind speed bar from blue to red
cbarLabel = cbar.set_label('Wind speed (m/s)')


plt.show()
plt.savefig(fname = 'ERA5map' + str(mapNumBegin)+ '.png')
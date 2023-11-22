#The purpose of this program is to create a master file consisting of analyzed ERA-5 maps.
#The program should take in ERA-5 files and then extract certain aspects to determine the average wind speed and wind direction on each map over the pre-determined South Georgia Island area.
#These results will then be pasted into a text file which will be referenced in later programs.
#Type 2 simply means that the majority of the code is not being referenced as a method, but rather in a massive double for loop as seen below.

import array as arr
import os.path
import sys
import time
from optparse import OptionParser

import matplotlib as matplotlib
import matplotlib.axes as ax
import matplotlib.pyplot as plt
import mysubs as ms  # get the file with all of my subroutines
import numpy as np
import pandas as pd
import readnc
from matplotlib.animation import FuncAnimation
from netCDF4 import Dataset
import datetime
from datetime import date, timedelta, datetime
# A prog to investigate the structure of the ERA5 u10/v10 files downloaded from Copernicus
# based on netcdf read code from census_8a.py

def timeDateDeterminer(currentMapNumber, w10):
    w10_pltCurrent = w10[currentMapNumber]  # used to determine beginning time
    daysChange = w10_pltCurrent / 24.
    #print(daysChange)
    newDTCurrent = timedelta(np.float64(daysChange))
    print(newDTCurrent)
    dtCurrent = datetime(1900, 1, 1) + newDTCurrent
    return str(dtCurrent)

completeName = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_mnspd_mndir_MASTER_NEW.txt')

ERA5_mnspd_mndir = open(completeName, "w+")
# time it from here
start_time = time.time()
for y in range(2000,2010): #sets the year
    for m in range(1,13): #sets the month
        print(m)
        file_name = '/Volumes/Blanken_HD/ERA5_Data/ERA5_downloads/' + str(y) + '_' + str(m).zfill(2) + '_uv.nc'
        print(file_name)  # prints file name to make sure output dates align with month being calculated
        ncfile = file_name
        try:
            nc_file = Dataset(ncfile, 'r')
            print("file is ok")
        except IOError:
            print('not a valid netCDF file')
            break
        #print(nc_file)
        [attr_list, global_attr] = readnc.readGlobalAttrs(nc_file)
        [vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)
        #print(vars)
        mapNumBegin = 0
        mapNumEnd = 0


        MapNumEnd_arr = np.zeros((2, 12), dtype=int)
        MapNumEnd_arr[0, :] = [123, 115, 123, 119, 123, 119, 123, 123, 119, 123, 119, 123] # leap year
        MapNumEnd_arr[1, :] = [123, 111, 123, 119, 123, 119, 123, 123, 119, 123, 119, 123] # non-leap year
        ifleap = 1
        if y % 4 == 0:
            ifleap = 0

        mapNumEnd = MapNumEnd_arr[ifleap, m-1]
        u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
        v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
        w10 = var_data_list[2]  # time for each data map
        print(w10)

        #ERA-5 plot limits
        #rowBegin = 523
        #rowEnd = 610
        #colBegin = 1198
        #colEnd = 1378
        #World map limits
        #rowBegin= 0
        #rowEnd = 720
        #colBegin = 0
        #colEnd = 1439
        # 200 km lat x 500 km long west of island
        rowBegin = 574
        rowEnd = 582
        colBegin = 1255
        colEnd = 1285

        for h in range(mapNumBegin, mapNumEnd+1):
            currentDateTime = timeDateDeterminer(h,w10)
            print('Map num: ' + str(h))
            map_spd = np.sqrt(u10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2) #determines map speed over all of the maps that it looks through
            map_spd_average = np.mean(map_spd)
            umean = np.mean(u10[h, rowBegin:rowEnd + 1, colBegin:colEnd + 1])
            vmean = np.mean(v10[h, rowBegin:rowEnd + 1, colBegin:colEnd + 1])
            dirmean = np.rad2deg(np.arctan2(vmean, umean))  # vector mean calculation in degrees
            if dirmean < 0:
                dirmean = dirmean + 360
            print('Map date & time: ' + currentDateTime)
            print('Map speed: ' + str(map_spd_average))
            print('Map direction: ' + str(dirmean))
            ERA5_mnspd_mndir.write(str(file_name) + ', ' + str(h).zfill(3) + ', ' + str(currentDateTime) + ', ' + str(int(map_spd_average)).zfill(2) + ', ' + str(int(dirmean)).zfill(3) + '\r\n') #writes to the text file
        nc_file.close()

ERA5_mnspd_mndir.close()


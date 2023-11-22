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
import os.path
from netCDF4 import Dataset
import MandNsubs as sub
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib

#  A prog to investigate the structure of the ERA5 u10/v10 files downloaded from Copernicus
# based on netcdf read code from census_8a.py

start_time = time.time()

#creates values for plotting axis of 2000 km plot
lat_coord_array = np.zeros(200, dtype=float) #initiates latitude values
long_coord_array = np.zeros(200, dtype=float) #initiates longitude values
coordinate_row = -45.3 #top left corner lat value
coordinate_col = 307.5 #top left corner long value
lat_resolution = 10/111.111
long_resolution = (10 / (111.111 * np.cos(np.deg2rad(54.3))))
for r in range (0,200):
    for c in range(0,200):
        #lat_coord_array[r] = coordinate_row
        #long_coord_array[c] = coordinate_col
        #coordinate_col += long_resolution
    #coordinate_row -= lat_resolution
    #coordinate_col = 307.5
        lat_coord_array[r] = 1000 - (r*10)
        long_coord_array[c] = (c*10) - 1000

#These linesare used to initiate certain variables used in later loops
conditional_file = '/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_mnspd_mndir_MASTER_NEW.txt'
conditional_file_variable = open(conditional_file, 'r')
all_lines = conditional_file_variable.readlines()
test_line = all_lines[0] #grabs a line which is used to initiate variables
conditional_file_variable.close()
last_name = test_line[0:58] #range for file extension
mapNum = int(test_line[60:63]) #range for map number
fline = test_line[0:58]
nc_file = Dataset(fline, 'r')
[vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)
u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s

#ERA-5 plot limits
#rowBegin= 523
#rowEnd = 610
#colBegin = 1198
#colEnd = 1378
#QuikSCAT plot limits
rowBegin= 556
rowEnd = 606
colBegin = 1256
colEnd = 1328
#2000 km plot limits
rowBegin = 541
rowEnd = 613
colBegin = 1230
colEnd = 1353
#World map limits
#rowBegin= 0
#rowEnd = 720
#colBegin = 0
#colEnd = 1439

plt_array = np.zeros((200,200), dtype = 'float') #initiates plot array
map_counter_array = np.zeros((200,200), dtype = 'int') #initiates map counter array
mapCounter = 0 # counter for how many maps fit the conditions

testLine = all_lines[0]
mapNum = int(testLine[60:63]) #range for map number
currentMapSpeed = int(testLine[86:88]) #initializes the current map speed variable
currentMapDirection = int(testLine[90:93]) #initializes the current map direction variable
currentHour = int(testLine[76:78])

#for loop to go through every line
for l in range(0,len(all_lines)): #using a low number at the moment to get tests to run faster

    currentLine = all_lines[l]
    print(currentLine)
    mapNum = int(currentLine[60:63])  # range for map number
    currentMapSpeed = int(currentLine[86:88])
    currentMapDirection = int(currentLine[90:93])
    currentHour = int(currentLine[76:78])

    if 8 <= currentMapSpeed <= 10 and (300 <= currentMapDirection <= 359 or 0 <= currentMapDirection <= 30):  # used to set conditions for pulling maps
    #if currentHour == 0:
        mapCounter += 1
        fline = currentLine[0:58]
        if last_name == fline: #checks to see if the file was already read or not
            print('File is same as before')
        else:
            print('File is different than before')
            nc_file = Dataset(fline, 'r')
            print(nc_file)
            last_name = fline
            [attr_list, global_attr] = readnc.readGlobalAttrs(nc_file)
            [vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)

        u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
        v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
        latArray = var_data_list[1] #ERA-lat array
        longArray = var_data_list[0] #ERA-5 long array
        for r in range (rowBegin, rowEnd+1): #goes through all of the ERA-5 range
            for c in range(colBegin,colEnd+1):
                row_index, col_index = sub.Two_thousand_km_index_finder(latArray[r],longArray[c]) #converts coordinate to 2000 km plot
                wind_speed = np.sqrt(u10[int(mapNum),r, c]**2 + v10[int(mapNum),r, c]**2)
                #print(r, c, latArray[r], longArray[c], wind_speed)
                #plt_array[row_index,col_index] += wind_speed #test case for plotting just ERA-5 data on 10 km plot.
                minimum_value = 2 #some random value to make sure that the wind speed at each location isn't already added onto
                if wind_speed != 0:
                    plt_array[row_index,col_index] += wind_speed #cell with wind speed
                    map_counter_array[row_index,col_index] += 1
        print('Map num: ' + str(mapNum))
        #print('Map speed: ' + str(np.mean(map_spd)))

        print("Line number: " + str(l+1))
        print('Maps counted: ' + str(mapCounter))
        print('Time elapsed: ' + str(time.time() - start_time))
        print('Percent complete: ' + str(float(float(l/14612)*100)))
plt_array = plt_array / mapCounter #averages 2000 km plot
plt_array = sub.interp_era5(np.flipud(plt_array),np.flipud(map_counter_array))

dataOutputFile = os.path.join('/Volumes/Blanken_HD/8_10_and_300_30_ERA_5_data_NEW.txt') #opens the file that is being written to
data = open(dataOutputFile, "w+")
for r in range(0,200):
    for c in range(0,200):
        print(r,c,plt_array[r,c]) #makes sure there is consistent data at each point in the plot
        data.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array[r,c]).zfill(12)+ '\r\n') #writes the speed data to the output text file
data.close()
print('Maps counted: ' + str(mapCounter))

plt.imshow(plt_array, extent = [long_coord_array[0], long_coord_array[199], lat_coord_array[199], lat_coord_array[0]], origin='lower', aspect= 1.0, cmap='gnuplot2', vmin = 0, vmax = 20)
cbar = plt.colorbar()
#plt.xlabel('latitude($^\circ$)')
#plt.ylabel('longitude($^\circ$)')
plt.ylabel('Disance from SGI (km)')
plt.xlabel('Distance from SGI (km)')



print("Average ERA-5 speed: " + str(np.mean(plt_array)))

plt.title('ERA-5 data NEW' + '\n' + '8-10 m/s and 300-30 degrees')

cbarLabel = cbar.set_label('Wind speed (m/s)')

plt.show()

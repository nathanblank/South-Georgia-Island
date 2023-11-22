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

#These linesare used to initiate certain variables used in later loops
conditional_file = '/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_mnspd_mndir_MASTER.txt'
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

wind_direction_counter_array = np.zeros((72), dtype = 'float') #initiates plot array
super_conditional_element_counter = 0 #counts 8-10 and 300-30 element number
testLine = all_lines[0]
mapNum = int(testLine[60:63]) #range for map number
currentMapSpeed = int(testLine[86:88]) #initializes the current map speed variable
currentMapDirection = int(testLine[90:93]) #initializes the current map direction variable
mapCounter = 0
element_counter = 0



#for loop to go through every line
for l in range(0, len(all_lines)): #using a low number at the moment to get tests to run faster
    currentLine = all_lines[l]
    mapNum = int(currentLine[60:63])  # range for map number
    currentMapSpeed = int(currentLine[86:88])
    currentMapDirection = int(currentLine[90:93])
    #if 8 <= currentMapSpeed <= 10 and (165 <= currentMapDirection <= 195):  # used to set conditions for pulling maps
    if 1==1:
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
                element_counter += 1
                wind_speed = np.sqrt(u10[int(mapNum),r, c]**2 + v10[int(mapNum),r, c]**2)
                wind_direction = np.rad2deg(np.arctan2(v10[mapNum,r,c],u10[mapNum,r,c]))
                if wind_direction < 0:
                    wind_direction += 360
                if 8 <= wind_speed <= 10 and ((300 <= wind_direction <= 359) or (0 <= wind_direction <= 30)):
                    super_conditional_element_counter += 1
                wind_direction_counter_array[int(wind_direction/5)] += 1
                #print('Wind direction: ' + str(wind_direction))

        print('Map num: ' + str(mapNum))
        #print('Map speed: ' + str(np.mean(map_spd)))

        print("Line number: " + str(l+1))
        print('Maps counted: ' + str(mapCounter))
        print('Time elapsed: ' + str(time.time() - start_time))
        print('Percent complete: ' + str(float(float(l/14612)*100)))


dataOutputFile = os.path.join('/Volumes/Blanken_HD/All_ERA_5_data_for_wind_direction_1D_histogram.txt') #opens the file that is being written to
data = open(dataOutputFile, "w+")
array_index = np.zeros(72, dtype = 'float')

for r in range(0,72):
    data.write(str(r).zfill(2) + ' ' + str(wind_direction_counter_array[r]) + '\n')
    print(wind_direction_counter_array[r])
    array_index[r] = r*5
    wind_direction_counter_array[r] = 100 * float(wind_direction_counter_array[r] / element_counter)
data.close()
print('Maps counted: ' + str(mapCounter))
print('Number of ERA-5 elements that hit 8-10 and 300-30: ' + str(super_conditional_element_counter))
print('Number of ERA-5 elements: ' + str(element_counter))
print('Percent of ERA-5 elements that hit 8-10 and 300-30: ' + str(100*super_conditional_element_counter/element_counter) + '%')
plt.plot(array_index, wind_direction_counter_array)

plt.xlabel('Wind Direction (degrees)')
plt.ylabel('Percent of Elements')
#print("Average ERA-5 speed: " + str(np.mean(plt_array)))
plt.axis([0, 355,0,5])
plt.title('Number of Elements at Each Wind Direction in ERA-5')

plt.show()

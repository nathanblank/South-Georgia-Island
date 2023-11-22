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

#These lines until the ERA-5 plot limits are used to initiate a test line for the u10 and v10 plots to be created off of as well as the 'last_line'
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
dataOutputFile = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ALL_ANALYZED_data.txt')
data = open(dataOutputFile, "w+")
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
# 2000 km plot limits
rowBegin = 541
rowEnd = 613
colBegin = 1230
colEnd = 1353
#World map limits
#rowBegin= 0
#rowEnd = 720
#colBegin = 0
#colEnd = 1439
u10_plt = u10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]  # defines u10_plt
v10_plt = v10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]  # defines v10_plt
spd_plt = np.sqrt(u10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2)
plt_array = np.zeros((200,200), dtype = 'float')
dirmean = np.rad2deg(np.arctan2(v10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1], u10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1]))
mapCounter = 0 # counter for how many maps fit the conditions

testLine = all_lines[0]
mapNum = int(testLine[60:63]) #range for map number
currentMapSpeed = int(testLine[86:88])
currentMapDirection = int(testLine[90:93])
#atmp = np.zeros([88,180], dtype=float)

#for loop to go through every line
for l in range(0, 14612):
    currentLine = all_lines[l]
    mapNum = int(currentLine[60:63])  # range for map number
    currentMapSpeed = int(currentLine[86:88])
    currentMapDirection = int(currentLine[90:93])
    if 8 <= currentMapSpeed <= 10 and (300 <= currentMapDirection <= 359 or 0 <= currentMapDirection <= 30):  # used to set conditions for pulling maps
        mapCounter += 1
        fline = currentLine[0:58]
        if last_name == fline: #checks to see if the file was already read or not
            print('File is same as before')
        else:
            print('File is different than before')
            nc_file = Dataset(fline, 'r')
            last_name = fline
            [attr_list, global_attr] = readnc.readGlobalAttrs(nc_file)
            [vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)

        u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
        v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s

        map_spd = np.sqrt(u10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1]**2 + v10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1]**2) #determines map speed over all of the maps that it looks through
        plt_array += map_spd

        umean = np.mean(u10[int(mapNum), rowBegin:rowEnd + 1, colBegin:colEnd + 1])
        vmean = np.mean(v10[int(mapNum), rowBegin:rowEnd + 1, colBegin:colEnd + 1])
        map_dir = np.rad2deg(np.arctan2(vmean,umean))  # vector mean calculation in degrees
        if map_dir < 0:
            map_dir = map_dir + 360
        dirmean += map_dir
        print('Map num: ' + str(mapNum))
        print('Map speed: ' + str(np.mean(map_spd)))
        print('Map direction: ' + str(map_dir))
        #u10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += u10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]
        #v10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += v10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]

        #atmp[rowBegin:rowEnd+1, colBegin:colEnd+1] += np.sqrt(u10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1]**2 + v10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1]**2)
        print("Line number: " + str(l+1))
        print('Maps counted: ' + str(mapCounter))
        print('Time elapsed: ' + str(time.time() - start_time))
        print('Percent complete: ' + str(float(float(l/14612)*100)))
        #print('spd plot shape 1: ' + str(spd_plt.shape))


#makes the MASK over SGI
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
    plt_array[row_index,col_index] = 0


#u10_plt = u10_plt / (mapCounter) #divides each coordinate point (array index) by however many maps were counted
#v10_plt = v10_plt / (mapCounter)
spd_plt = spd_plt / mapCounter
dirmean = np.mean(dirmean)
for r in range(0,(rowEnd - rowBegin)+1):
    for c in range(0, (colEnd-colBegin)+1):
        data.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(spd_plt[r,c]).zfill(12)+ '\r\n')

data.close()

#tmp_mean = np.mean(spd_plt)
aatmp = np.flipud(spd_plt)

#print('Mean wind speed: ' + str(tmp_mean))
print('Maps counted: ' + str(mapCounter))
print("Average direction: " + str(dirmean))
#These two lines are used to set the proper axis (degrees) for the plot
longArray = var_data_list[0]
latArray = var_data_list[1]

#fig = plt.figure()


plt.imshow(aatmp, extent = [longArray[colBegin], longArray[colEnd], latArray[rowEnd], latArray[rowBegin]], origin='lower', aspect= 2.0, cmap='nipy_spectral')
cbar = plt.colorbar()
plt.xlabel('latitude($^\circ$)')
plt.ylabel('longitude($^\circ$)')


plt.title('Average Wind Speeds of 8-10 m/s and 300-30 degrees Data')

cbarLabel = cbar.set_label('Wind speed (m/s)')

plt.show()

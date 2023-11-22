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
dataOutputFile1 = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/8to10_300_330_data_2000KM.txt')
data1 = open(dataOutputFile1, "w+")
dataOutputFile2 = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/8to10_330_359_data_2000KM.txt')
data2 = open(dataOutputFile2, "w+")
dataOutputFile3 = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/8to10_0_30_data_2000KM.txt')
data3 = open(dataOutputFile3, "w+")
#ERA-5 plot limits
#rowBegin= 523
#rowEnd = 610
#colBegin = 1198
#colEnd = 1378
#QuikSCAT plot limits
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
spd_plt1 = np.sqrt(u10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2)
spd_plt2 = np.sqrt(u10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2)
spd_plt3 = np.sqrt(u10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]**2)
mapCounter1 = 0 # counter for how many maps fit the conditions
mapCounter2 = 0
mapCounter3 = 0
#atmp = np.zeros([88,180], dtype=float)

#for loop to go through every line
for l in range(0, 14612):
    currentLine = all_lines[l]
    mapNum = int(currentLine[60:63]) #range for map number
    currentMapSpeed = int(currentLine[86:88])
    currentMapDirection = int(currentLine[90:93])
    #print(currentMapDirection, currentMapSpeed, mapCounter1, mapCounter2, mapCounter3)
    if 8 <= currentMapSpeed <= 10 and (300 <= currentMapDirection <= 359 or 0 <= currentMapDirection <= 30) :  # used to set conditions for pulling maps
        fline = currentLine[0:58]
        if last_name == fline:  # checks to see if the file was already read or not
            print('File is same as before')
        else:
            print('File is different than before')
            nc_file = Dataset(fline, 'r')
            last_name = fline
            [attr_list, global_attr] = readnc.readGlobalAttrs(nc_file)
            [vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)
        u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
        v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
        
        if 300 <= currentMapDirection <= 330:
            subSection = 1
            print(currentMapDirection, subSection)
            map_spd1 = np.sqrt(u10[int(mapNum), rowBegin:rowEnd + 1, colBegin:colEnd + 1] ** 2 + v10[int(mapNum), rowBegin:rowEnd + 1,colBegin:colEnd + 1] ** 2)  # determines map speed over all of the maps that it looks through
            spd_plt1 += map_spd1
            mapCounter1 += 1

        if 331 <= currentMapDirection <= 359:
            subSection = 2
            print(currentMapDirection, subSection)
            map_spd2 = np.sqrt(u10[int(mapNum), rowBegin:rowEnd + 1, colBegin:colEnd + 1] ** 2 + v10[int(mapNum), rowBegin:rowEnd + 1, colBegin:colEnd + 1] ** 2)  # determines map speed over all of the maps that it looks through
            spd_plt2 += map_spd2
            mapCounter2 += 1

        if 0 <= currentMapDirection <= 30:
            subSection = 3
            print(currentMapDirection, subSection)
            map_spd3 = np.sqrt(u10[int(mapNum), rowBegin:rowEnd + 1, colBegin:colEnd + 1] ** 2 + v10[int(mapNum), rowBegin:rowEnd + 1, colBegin:colEnd + 1] ** 2)  # determines map speed over all of the maps that it looks through
            spd_plt3 += map_spd3
            mapCounter3 += 1

        #print('Map num: ' + str(mapNum))

        # u10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += u10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]
        # v10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += v10[int(mapNum),rowBegin:rowEnd+1,colBegin:colEnd+1]

        # atmp[rowBegin:rowEnd+1, colBegin:colEnd+1] += np.sqrt(u10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1]**2 + v10[int(mapNum),rowBegin:rowEnd+1, colBegin:colEnd+1]**2)
        print("Line number: " + str(l + 1))
        print('Maps counted: ' + str(np.sum(mapCounter1 + mapCounter2 + mapCounter3)))
        print('Time elapsed: ' + str(time.time() - start_time))
        print('Percent complete: ' + str(float(float(l / 14612) * 100)))

#u10_plt = u10_plt / (mapCounter) #divides each coordinate point (array index) by however many maps were counted
#v10_plt = v10_plt / (mapCounter)
spd_plt1 = spd_plt1 / mapCounter1
spd_plt2 = spd_plt2 / mapCounter2
spd_plt3 = spd_plt3 / mapCounter3
print('Map 1s counted: ' + str(mapCounter1))
print('Map 2s counted: ' + str(mapCounter2))
print('Map 3s counted: ' + str(mapCounter3))

#Makes the (200,200) plots
plt_array1 = np.zeros((200,200), dtype = 'float')
plt_array2 = np.zeros((200,200), dtype = 'float')
plt_array3 = np.zeros((200,200), dtype = 'float')
for r in range(rowBegin, rowEnd):
    for c in range(colBegin, colEnd):
        row_index, col_index = sub.ERA5_index_finder_2000_km_plot_region(r,c)
        plt_array1[row_index, col_index] = spd_plt1[r, c]
        plt_array2[row_index, col_index] = spd_plt2[r, c]
        plt_array3[row_index, col_index] = spd_plt3[r, c]

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
    plt_array1[row_index,col_index] = 0
    plt_array2[row_index, col_index] = 0
    plt_array3[row_index, col_index] = 0


#tmp_mean = np.mean(spd_plt)
aatmp1 = np.flipud(spd_plt1)
aatmp2 = np.flipud(spd_plt2)
aatmp3 = np.flipud(spd_plt3)
#print('Mean wind speed: ' + str(tmp_mean))
print('Maps counted: ' + str(mapCounter1 + mapCounter2 + mapCounter3))
#These two lines are used to set the proper axis (degrees) for the plot
longArray = var_data_list[0]
latArray = var_data_list[1]

#fig = plt.figure()
for r in range(0,200):
    for c in range(0, 200):
        data1.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array1[r, c]).zfill(12)+ '\r\n')
        data2.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array2[r, c]).zfill(12) + '\r\n')
        data3.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array3[r, c]).zfill(12) + '\r\n')
data1.close()
data2.close()
data3.close()

plt.figure(figsize=(18,5))
TNRfont = {'fontname': 'Times New Roman'}
plt.subplot(131)
plot1 = plt.imshow(plt_array1, extent = [long_coord_array[colBegin], long_coord_array[colEnd], lat_coord_array[rowEnd], lat_coord_array[rowBegin]], origin='lower', aspect= 2.0, cmap='nipy_spectral')
cbar = plt.colorbar(plot1, fraction=0.05, pad=0.04)
plt.title('300-330 degrees',fontsize=16, **TNRfont)

plt.subplot(132)
plot2 = plt.imshow(plt_array2, extent = [long_coord_array[colBegin], long_coord_array[colEnd], lat_coord_array[rowEnd], lat_coord_array[rowBegin]], origin='lower', aspect= 2.0, cmap='nipy_spectral')
cbar = plt.colorbar(plot2, fraction=0.05, pad=0.04)
plt.title('331-359 degrees',fontsize=16, **TNRfont)
plt.subplot(133)
plot3 = plt.imshow(plt_array3, extent = [long_coord_array[colBegin], long_coord_array[colEnd], lat_coord_array[rowEnd], lat_coord_array[rowBegin]], origin='lower', aspect= 2.0, cmap='nipy_spectral')
cbar = plt.colorbar(plot3, fraction=0.05, pad=0.04)
plt.title('0-30 degrees',fontsize=16, **TNRfont)

plt.suptitle('Average Wind Speeds 8 to 10 m/s', fontsize=32, **TNRfont)


#plot = plt.figure(figsize=(6.1, 5.4), dpi=100)
plt.ylabel('latitude($^\circ$)', fontsize=16, **TNRfont)
plt.xlabel('longitude($^\circ$)', fontsize=16, **TNRfont)
cbarLabel = cbar.set_label('Wind speed (m/s)', fontsize=16, **TNRfont)
plt.tick_params(axis='both', labelsize=16)
cbar.ax.tick_params(axis='y', labelsize=16)
plt.savefig('ERA_5.svg', dpi=100)
plt.show()
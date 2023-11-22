import numpy as np
import MandNsubs as sub
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
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib

#  A prog to investigate the structure of the ERA5 u10/v10 files downloaded from Copernicus
# based on netcdf read code from census_8a.py

start_time = time.time()
#Used to get var_data_list 0 and 1 for proper axis
conditional_file1 = '/Volumes/Blanken_HD/ERA5_Data/ERA5_downloads/2000_01_uv.nc' #random ERA-5 file to grab arrays

nc_file = Dataset(conditional_file1, 'r')
[vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)
#These lines until the ERA-5 plot limits are used to initiate a test line for the u10 and v10 plots to be created off of as well as the 'last_line'
conditional_file2 = '/Volumes/Blanken_HD/ERA5_Output_Data/8to10_0_30_data.txt' #input text file from analyzed ERA-5 map (conditional mean map)
conditional_file_variable2 = open(conditional_file2, 'r')
all_lines = conditional_file_variable2.readlines()
test_line = all_lines[0]
rowNum = int(test_line[0:3])
colNum = int(test_line[4:7])
spd_plt = np.zeros((51,73), dtype = float)
dirmean = 0
for l in range(len(all_lines)):
    currentLine = all_lines[l]
    rowNum = int(currentLine[0:3])
    colNum = int(currentLine[4:7])
    dirmean += np.rad2deg(np.arctan2(int(currentLine[8:21]), 1))
    if dirmean < 0:
        dirmean = dirmean + 360
    spd_plt[rowNum,colNum] = float(currentLine[8:21])
    print(rowNum,colNum, spd_plt[rowNum,colNum])
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
#World map limits
#rowBegin= 0
#rowEnd = 720
#colBegin = 0
#colEnd = 1439

#This is the part that makes SGI a specific color

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
    spd_plt[row_index,col_index] = 0


#tmp_mean = np.mean(spd_plt)
aatmp = np.flipud(spd_plt)

#These two lines are used to set the proper axis (degrees) for the plot
longArray = var_data_list[0]
latArray = var_data_list[1]



plt.imshow(aatmp, extent = [longArray[colBegin], longArray[colEnd], latArray[rowEnd], latArray[rowBegin]], origin='lower', aspect= 2.0, cmap='nipy_spectral')
cbar = plt.colorbar()
plt.ylabel('latitude($^\circ$)')
plt.xlabel('longitude($^\circ$)')


plt.title('Average Wind Speeds 8-10 m/s and 0-30 degrees')

cbarLabel = cbar.set_label('Wind speed (m/s)')

plt.show()

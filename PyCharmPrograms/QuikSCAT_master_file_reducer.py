#This program creates a text file that outputs the file path of the QuikSCAT rev as well as how many points hit inside the SGI region
#The first section of numbers is how many points hit if the rev was an ascending rev and the second set is for if it was a descending rev
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

start_time = time.time()  # determines starting time
in_text_file = "/Volumes/Blanken_HD/QuikSCAT_Master_Master.txt"
out_file = "/Volumes/Blanken_HD/REDUCED_master_file_2_0.txt"

"""
Coordinates: (lat,long)
SGI: -54.3, -27.1
Lat range: -45.3 to -63.3
Long range:-17.1 to -57.1 (342.9 to 302.9)

This outputs a text file with each line being a QuikSCAT absolute path name 0:99, number of ascending path points 100:106 and decending number of points 106:113
"""


read_in_file = open(in_text_file, 'r')
read_out_file = open(out_file, 'w+')
all_lines = read_in_file.readlines()
test_line = all_lines[0] #grabs a line which is used to initiate variables
exceptions_counter = 0
for l in range(0,len(all_lines)):
    currentLine = all_lines[l]
    try:
        nc_file = Dataset(currentLine[0:99], 'r')
       # print("file is ok")
    except IOError:
        print('not a valid netCDF file')
    #print(nc_file)

   # print(currentLine[0:99]) #prints file name
    [attr_list, global_attr] = readnc.readGlobalAttrs(nc_file)
    [vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)
    time_Array = var_data_list[0]
    lat_Array = var_data_list[1]
    long_Array = var_data_list[2]
    windSpeed_Array = var_data_list[3]
    windDirection_Array = var_data_list[4]
    rain_Array = var_data_list[5]
    flags_Array = var_data_list[6]

    Long_ascending_arr = long_Array[237:425, :]

    ascending_value = np.where((Long_ascending_arr >= 302) & (Long_ascending_arr <= 343))
    ascending_value = np.asarray(ascending_value)
    #print('Ascending: ' + str(ascending_value[0].size))
    Long_descending_arr = long_Array[2823:3011, :]
    descending_value = np.where((Long_descending_arr >= 302) & (Long_descending_arr <= 343))
    descending_value = np.asarray(descending_value)
    #print('Descending: ' + str(descending_value[0].size))

    if ascending_value[0].size > 0 or descending_value[0].size > 0:
        print(currentLine[0:99])  # prints file name
        print('Ascending: ' + str(ascending_value[0].size))
        print('Descending: ' + str(descending_value[0].size))
        read_out_file.write(str(currentLine[0:99]) + ' ' + str(len(ascending_value[0])).zfill(5) + ' ' + str(len(descending_value[0])).zfill(5) + '\r\n')
    if ascending_value[0].size > 0 and descending_value[0].size > 0:
        print(currentLine[0:99])  # prints file name
        print('**************************')
        print('Ascending: ' + str(ascending_value[0].size))
        print('Descending: ' + str(descending_value[0].size))
        print('**************************')
        exceptions_counter += 1
    if l % 1000 == 0:
        print('**************************')
        print("Exceptions: " + str(exceptions_counter))
        print('**************************')
    if l % 50 == 0:
        print('Time: ' + str(time.time() - start_time))
        print('Percent complete: ' + str((l/52496) * 100) + '%')
        print('Files complete: ' + str(l) + '/52496')
print("Exceptions: " + str(exceptions_counter))



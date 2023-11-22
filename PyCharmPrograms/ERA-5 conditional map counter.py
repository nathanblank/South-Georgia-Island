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



conditional_file = '/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_mnspd_mndir_MASTER.txt'

conditional_file_variable = open(conditional_file, 'r')
all_lines = conditional_file_variable.readlines()
test_line = all_lines[0] #grabs a line which is used to initiate variables
conditional_file_variable.close()

mapCounter = 0 # counter for how many maps fit the conditions


mapNum = int(test_line[60:63]) #range for map number
currentMapSpeed = int(test_line[86:88]) #initializes the current map speed variable
currentMapDirection = int(test_line[90:93]) #initializes the current map direction variable

start_speed = 8
end_speed = 10
start_direction1 = 300
end_direction1 = 359
start_direction2 = 0
end_direction2 = 30

#for loop to go through every line
for l in range(0, len(all_lines)): #using a low number at the moment to get tests to run faster
    currentLine = all_lines[l]
    mapNum = int(currentLine[60:63])  # range for map number
    currentMapSpeed = int(currentLine[86:88])
    currentMapDirection = int(currentLine[90:93])
    if start_speed <= currentMapSpeed <= end_speed and (start_direction1 <= currentMapDirection <= end_direction1 or start_direction2 <= currentMapDirection <= end_direction2):  # used to set conditions for pulling maps
        mapCounter += 1

print("Number of ERA-5 maps that meet conditions " +str(start_speed) + '-' + str(end_speed) + ', ' + str(start_direction1) + '-' + str(end_direction1) + ' and, ' + str(start_direction2) + '-' + str(end_direction2) + ' = ' + str(mapCounter))


#This program makes a 1D histogram of the number of points that each QuikSCAT rev has when it goes over the SGI region
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
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib


#time and date is range char [60,79]
#wind speed is range [86,88]
#wind direction is range [90,93]

in_text_file= "/Volumes/Blanken_HD/REDUCED_master_file_2_0.txt"


num_points_array = np.zeros((290), dtype = int)
inline = open(in_text_file, 'r')
line = inline.readlines()


for l in range (0,22178):
    currentLine = line[l]
    ascending_points = int(currentLine[100:106])
    print("Ascending: " + str(ascending_points))
    descending_points = int(currentLine[106:113])
    print("Descending: " + str(descending_points))
    num_points_at_line = int((int(currentLine[100:106]) + int(currentLine[106:113])) / 100)
    num_points_array[num_points_at_line] += 1

index = np.arange(len(num_points_array))
for e in range(0,290):
    print(e,num_points_array[e])
plt.bar(index, num_points_array,  align='center', data=None)
plt.ylim(0,800)
plt.xlim(0,290)
plt.title(('Bar Graph of Number of Points of SGI Region in each QuikSCAT Rev'), fontdict=None, loc='center', pad=None)
plt.xlabel('Number of Points (100s)')
plt.ylabel('Count')
plt.show()


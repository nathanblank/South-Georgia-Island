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
import MandNsubs as sub
from netCDF4 import Dataset
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib

in_ERA_5_file = '/Users/N-Dogg/Documents/All_ERA_5_data_for_wind_speed_1D_histogram_CONFIRMED.txt'
read_in_file = open(in_ERA_5_file, 'r')
all_ERA_5_lines = read_in_file.readlines()
currentLine = all_ERA_5_lines[0]
index = currentLine[0:3]
element_count = currentLine[4:15]
index_array = np.zeros(150, dtype = 'float')
element_count_array = np.zeros(150, dtype = 'float')

for l in range(150):
    currentLine = all_ERA_5_lines[l]
    index = float(int(currentLine[0:3]) / 4)
    element_count = int(currentLine[3:15])
    index_array[l] = index
    element_count_array[l] = element_count
    print(index,element_count)

total_number_elements = np.sum(element_count_array)  #finds total number of elements covered
print(total_number_elements)


for l in range(150):
    element_count_array[l] /= total_number_elements #divides each point by total number of elements
element_count_array *= 100 #multiplys by 100 to find %





in_QuikSCAT_file = '/Users/N-Dogg/Documents/ALL_QuikSCAT_1D_histogram_data_CONFIRMED.txt'

QuikSCAT_read_in_file = open(in_QuikSCAT_file, 'r')
all_QuikSCAT_lines = QuikSCAT_read_in_file.readlines()
QuikSCAT_currentLine = all_QuikSCAT_lines[0]
QuikSCAT_index = QuikSCAT_currentLine[0:3]
QuikSCAT_element_count = QuikSCAT_currentLine[4:15]
QuikSCAT_index_array = np.zeros(150, dtype = 'float')
QuikSCAT_element_count_array = np.zeros(150, dtype = 'float')

for l in range(150):
    QuikSCAT_currentLine = all_QuikSCAT_lines[l]
    QuikSCAT_index = float(int(QuikSCAT_currentLine[0:3])/4)
    QuikSCAT_element_count = int(QuikSCAT_currentLine[3:15])
    QuikSCAT_index_array[l] = QuikSCAT_index
    QuikSCAT_element_count_array[l] = QuikSCAT_element_count
    print(l,QuikSCAT_index,QuikSCAT_element_count)

QuikSCAT_total_number_elements = np.sum(QuikSCAT_element_count_array)  #finds total number of elements covered
print(QuikSCAT_total_number_elements)

for l in range(150):
    QuikSCAT_element_count_array[l] /= QuikSCAT_total_number_elements #divides each point by total number of elements
QuikSCAT_element_count_array *= 100 #multiplys by 100 to find %






for r in range(150):
    print(r,element_count_array[r],QuikSCAT_element_count_array[r])

plt.plot(index_array, element_count_array,'r-', label = 'ERA-5' )
plt.plot(QuikSCAT_index_array, QuikSCAT_element_count_array, 'b-.', label = 'QuikSCAT' )
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Percent of Element (%)')
plt.title('Percent of Elements at Each Wind Speed in ERA-5 and QuikSCAT')

plt.legend(loc='upper right', shadow=True, fontsize='x-large')

plt.axis([0, 25,0,3])
#plt.fill_between(8,element_count_array, color= 'red') #highlights condition
plt.show()

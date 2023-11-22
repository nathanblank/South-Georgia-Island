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

in_file = '/Volumes/Blanken_HD/All_ERA_5_data_for_wind_direction_1D_histogram_CONFIRMED_TEST.txt'
QuikSCAT = False
read_in_file = open(in_file, 'r')
all_lines = read_in_file.readlines()
currentLine = all_lines[0]
index = currentLine[0:3]
#wind direction
element_count = currentLine[4:15]
index_array = np.zeros(72, dtype = 'float')
element_count_array = np.zeros(72, dtype = 'float')



for l in range(72):

    currentLine = all_lines[l]

    index = float(int(currentLine[0:2]) * 5) - 180 #wind direction

    element_count = float(currentLine[3:20]) #wind direction

    index_array[l] = index
    element_count_array[l] = element_count
    print(currentLine[0:2],currentLine[3:20])
    print(index,element_count)
    print()
    print()

total_number_elements = np.sum(element_count_array)  #finds total number of elements covered
print(total_number_elements)

#This set of code will add up the number of elemts in a certain wind direction
conditional_element_counter = 0
for l in range(0,72): #wind direction

    if -180 <= float(l*5) <= -120 or 0 <= float(l*5) <= 30: #wind direction

        conditional_element_counter += element_count_array[l]
        print(element_count_array[l], conditional_element_counter)
print('Elements in conditional range: ' + str(conditional_element_counter))
percent_of_conditional_elements = 100 * conditional_element_counter / total_number_elements
print('Percent of elements in conditional range: ' + str(percent_of_conditional_elements) + '%')

for l in range(72): #wind direction

    element_count_array[l] /= total_number_elements #divides each point by total number of elements
element_count_array *= 100 #multiplys by 100 to find %




if QuikSCAT == True:
    plt.plot(index_array, element_count_array)
else:
    plt.plot(index_array, element_count_array)
    plt.xlabel('Wind Direction (degrees)')

    plt.ylabel('Percent of Element (%)')

    plt.title('Percent of Elements at Each Wind Direction in ERA-5')
plt.axis([-180, 175,0,5])
#plt.axis([0,20,0,3])
#plt.fill_between(-30,element_count_array, color= 'red') #highlights condition
#plt.fill_between(30,element_count_array, color= 'red') #highlights condition
plt.show()



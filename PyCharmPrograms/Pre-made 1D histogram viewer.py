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

in_file = '/Volumes/Blanken_HD/All_ERA_5_data_for_wind_direction_1D_histogram_CONFIRMED.txt'
QuikSCAT = False
read_in_file = open(in_file, 'r')
all_lines = read_in_file.readlines()
currentLine = all_lines[0]
index = currentLine[0:3]
#wind direction
element_count = currentLine[4:15]
index_array = np.zeros(72, dtype = 'float')
element_count_array = np.zeros(72, dtype = 'float')
#wind speed
#element_count = currentLine[4:17]
#index_array = np.zeros(150, dtype = 'float')
#element_count_array = np.zeros(150, dtype = 'float')


for l in range(72):
#for l in range(150):
    currentLine = all_lines[l]
    index = float(int(currentLine[0:3]) * 5) #wind direction
    if index > 180:
        index = index - 360
    #index = float(int(currentLine[0:3]) / 4) #wind speed
    #element_count = int(currentLine[3:15]) #wind speed
    element_count = float(currentLine[3:20]) #wind direction
    adjusted_l = l + 36
    if l == 36:
        continue
    if adjusted_l >= 72:
        index_array[adjusted_l - 72] = index
        element_count_array[adjusted_l-72] = element_count
    else:
        index_array[adjusted_l] = index
        element_count_array[adjusted_l] = element_count
print(index,element_count)

total_number_elements = np.sum(element_count_array)  #finds total number of elements covered
print(total_number_elements)

#This set of code will add up the number of elemts in a certain wind speed
conditional_element_counter = 0
for l in range(0,72): #wind direction
#for l in range(150): #wind speed
    if -180 <= float(l*5) <= -120 or 0 <= float(l*5) <= 30: #wind direction
    #if 8 <= float(l/4) <= 10: #wind speed
        conditional_element_counter += element_count_array[l]
        print(element_count_array[l], conditional_element_counter)
print('Elements in conditional range: ' + str(conditional_element_counter))
percent_of_conditional_elements = 100 * conditional_element_counter / total_number_elements
print('Percent of elements in conditional range: ' + str(percent_of_conditional_elements) + '%')

for l in range(72): #wind direction
#for l in range(150): #wind speed
    element_count_array[l] /= total_number_elements #divides each point by total number of elements
element_count_array *= 100 #multiplys by 100 to find %




if QuikSCAT == True:
    plt.plot(index_array, element_count_array)
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Percent of Elements (%)')
    plt.title('Number of Elements at Each Wind Speed in QuikSCAT')
else:
    plt.plot(index_array, element_count_array)
    plt.xlabel('Wind Direction (degrees)')
    #plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Percent of Element (%)')
    #plt.title('Percent of Elements at Each Wind Speed in ERA-5')
    plt.title('Percent of Elements at Each Wind Direction in ERA-5')
plt.axis([-180, 180,0,5])
#plt.axis([0,20,0,3])
#plt.fill_between(8,element_count_array, color= 'red') #highlights condition
plt.show()



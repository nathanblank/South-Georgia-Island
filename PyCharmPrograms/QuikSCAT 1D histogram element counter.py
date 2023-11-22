#This program creates a 1D plot of the number of the speed of elements from all of the QuikSCAT revs that hit inside the SGI region.
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



# time it from here
start_time = time.time()


master_file_in = '/Volumes/Blanken_HD/Combined_ERA_5_and_QuikSCAT_Master_Version_2.txt' #master file pathname
read_master_file = open(master_file_in, 'r') #reads it
all_lines = read_master_file.readlines() #reads all lines
current_QuikSCAT_name = '' #initiates QuikSCAT name
current_ERA_5_name = '' #initiates ERA-5 name
ERA_5_wind_speed = 0 #initiates ERA-5 wind speed
ERA_5_wind_direction = 0 #initiates ERA-5 wind direction
QuikSCAT_ascending_point_value = 0 #initiates number of QuiKSCAT ascending points
QuikSCAT_descending_point_value = 0 #initiates number of QuikSCAT descening points
QuikSCAT_revs_counted = 0 #Counter to check how many QuikSCAT revs hit the condition
number_of_following_QuikSCAT_revs = 0 #number of revs after a certain ERA-5 map
element_counter = 0
wind_speed_counter_array = np.zeros(150, dtype = 'int')
index_tracker = np.zeros(150, dtype = 'float')

for r in range(0, 150):
    index_tracker[r] = float(r / 4)

for l in range(0, len(all_lines)): #going through however many number of lines (first QuikSCAT rev on line 18)
    currentLine = all_lines[l] #pulls current line from master file
    number_of_following_QuikSCAT_revs = currentLine[0:1] #determines how many QuikSCAT revs follow
    if number_of_following_QuikSCAT_revs == '/': #if the line's first character is a '/', then it continues to the next line
        continue
    print(number_of_following_QuikSCAT_revs, l) #otherwise it prints the number of following lines and line number

    current_ERA_5_name = currentLine[2:60] #current ERA-5 name
    ERA_5_wind_speed = int(currentLine[88:90]) #wind speed
    ERA_5_wind_direction = int(currentLine[92:96]) #wind direction
    #if 8 <= ERA_5_wind_speed <= 10 and (165 <= ERA_5_wind_direction <= 195): #checking if the ERA-5 map fits the conditions
    if 1==1:
        #print('objective 1')
        for q in range(0,int(number_of_following_QuikSCAT_revs)): #going though all of the QuikSCAT files that follow that ERA-5 line
             QuikSCAT_line = l + q + 1 #determining what the QuikSCAT line number is
             print('QuikSCAT rev on line: ' + str(QuikSCAT_line))
             currentLine = all_lines[QuikSCAT_line] #pulls current QuikSCAT line
             current_QuikSCAT_name = currentLine[0:99] #pulls QuikSCAT name
             try: #reads the QuikSCAT file
                nc_file = Dataset( current_QuikSCAT_name, 'r' )
                print("file is ok")
             except IOError:
                print('not a valid netCDF file')
             #print(nc_file)

             [attr_list, global_attr] = readnc.readGlobalAttrs( nc_file ) #unpacks QuikSCAT
             [vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )

             #initializes arrays
             time_Array = var_data_list[0]
             lat_Array = var_data_list[1]
             long_Array = var_data_list[2]
             windSpeed_Array = var_data_list[3]
             windDirection_Array = var_data_list[4]
             rain_Array = var_data_list[5]
             flags_Array = var_data_list[6]

             # used to determine where the satelitte goes over SGI so that way we know where to look for the data over SGI
             #print(currentLine[100:106])
             if int(currentLine[100:106]) > 0:
                 # ascending QuikSCAT limits
                 rowBegin = 190
                 rowEnd = 425
                 colBegin = 0
                 colEnd = 152
             else:
                 # descending QuikSCAT limits
                 rowBegin = 2823
                 rowEnd = 3058
                 colBegin = 0
                 colEnd = 152
             #print('objective 2')

             #going through the SGI range
             for r in range(rowBegin, rowEnd):
                 for c in range(colBegin, colEnd):
                     if long_Array[r, c] < 338.3: #checking for values that meet long range
                         if long_Array[r, c] > 307.5:
                             if lat_Array[r, c] < -45.3:#checking for values that meet lat range
                                 if lat_Array[r, c] > -63.3:
                                     if flags_Array[r,c] == 0:
                                         print('r: ' + str(r) + ', c: ' + str(c))
                                         row_index, col_index = sub.Two_thousand_km_index_finder(lat_Array[r, c],long_Array[r, c]) #determining plot coordinates
                                         print("Coordinate: (" + str(sub.truncate(lat_Array[r, c], 4)) + ", " + str(sub.truncate(long_Array[r, c], 4)) + ") is index: (" + str(row_index) + ", " + str(col_index) + ")") #just showing what index values the coordinates fall into
                                         try: #plotting wind speed. Has to be in try because of NaN values (that's what I found works, otherwise it throws a maskedArray error)
                                             if windSpeed_Array[r, c] != 0:  # if the wind speed doesn't equal 0, add one to that spot in the dividing array
                                                 wind_speed_counter_array[int(windSpeed_Array[r,c] * 4)] += 1
                                                 element_counter += 1
                                         except:
                                             print("Out of range")
                                         print()
                                         print()


        QuikSCAT_revs_counted += int(number_of_following_QuikSCAT_revs) #add the number of QuikSCAT revs counted
        print(QuikSCAT_revs_counted) #print it
output_file = '/Volumes/Blanken_HD/ALL_QuikSCAT_1D_histogram data.txt'
read_output_file = open(output_file, 'w+')

for r in range(0, 150):
    index_tracker[r] = float(r / 4)
    read_output_file.write(str(r).zfill(2) + ' ' + str(wind_speed_counter_array[r]) + '\n') #writes out [0:3] of row value, [4:7] col value and a guaranteed [8:16] of the wind speed

read_output_file.close()

print('Number of revs counted: ' + str(QuikSCAT_revs_counted)) #print it
print("time: " + str(time.time()-start_time))
TNRfont = {'fontname':'Times New Roman'}
params = plt.rcParams
plot = plt.figure(dpi=100)
plt.rcParams.update({'font.family': 'Times New Roman'})
plot_variable = plt.plot(index_tracker, wind_speed_counter_array)
plt.ylabel('Number of Elements')
plt.xlabel('Wind Speed (m/s)')
plt.title(('Number of Elements at Each Wind Speed in QuikSCAT'))
print('Number of QuikSCAT elements: ' + str(element_counter))


#plt.savefig('QuikSCAT_Averaged_0_30.svg', dpi=100)
plt.show()

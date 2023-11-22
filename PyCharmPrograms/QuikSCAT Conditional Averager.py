#This program creates conditional climatology plots for varying wind speeds and wind directions and write the 200 element by 200 element into a text file for future use.
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
from matplotlib.colors import LogNorm


# time it from here
start_time = time.time()

#creates values for plotting axis of 2000 km plot
lat_coord_array = np.zeros(200, dtype=float) #initiates latitude values
long_coord_array = np.zeros(200, dtype=float) #initiates longitude values
coordinate_row = -45.3 #top left corner lat value
coordinate_col = 307.5 #top left corner long value
lat_resolution = 10/111.111
long_resolution = (10 / (111.111 * np.cos(np.deg2rad(54.3))))
for r in range (0,200):
    for c in range(0,200):
        #lat_coord_array[r] = coordinate_row
        #long_coord_array[c] = coordinate_col
        #coordinate_col += long_resolution
    #coordinate_row -= lat_resolution
    #coordinate_col = 307.5
        lat_coord_array[r] = 1000 - (r * 10)
        long_coord_array[c] = (c * 10) - 1000

max_speed = 0
min_speed = 100
total_elements = 0
dividing_array = np.zeros((200, 200),dtype='int')  # makes array which will be used to find average plot. The reason I have an array for this is because not all points in the plot get hit by every QuikSCAT rev, so when a point does get hit by one, it adds one to the dividing array at that point, and then the value at that point is used to later divide the sum of the speeds at that point
master_file_in = '/Volumes/Blanken_HD/Combined_ERA_5_and_QuikSCAT_Master_Version_2_NEW.txt' #master file pathname
read_master_file = open(master_file_in, 'r') #reads it
all_lines = read_master_file.readlines() #reads all lines
current_QuikSCAT_name = '' #initiates QuikSCAT name
current_ERA_5_name = '' #initiates ERA-5 name
ERA_5_wind_speed = 0 #initiates ERA-5 wind speed
ERA_5_wind_direction = 0 #initiates ERA-5 wind direction
QuikSCAT_ascending_point_value = 0 #initiates number of QuiKSCAT ascending points
QuikSCAT_descending_point_value = 0 #initiates number of QuikSCAT descening points
plt_array = np.zeros((200,200), dtype='float') #makes 2000 km plotting array
QuikSCAT_revs_counted = 0 #Counter to check how many QuikSCAT revs hit the condition
number_of_following_QuikSCAT_revs = 0 #number of revs after a certain ERA-5 map


for l in range(0,len(all_lines)):

    print()
    print()
    print("Overall line: " + str(l))
    currentLine = all_lines[l] #pulls current line from master file
    if currentLine == '':
        continue
    number_of_following_QuikSCAT_revs = currentLine[0:1] #determines how many QuikSCAT revs follow

    if number_of_following_QuikSCAT_revs == '/': #if the line's first character is a '/', then it continues to the next line
        continue
    else:
        current_ERA_5_time = int(currentLine[78:80])
        #print(current_ERA_5_time)
    #print(number_of_following_QuikSCAT_revs, l) #otherwise it prints the number of following lines and line number

    fline = currentLine[2:60] #current ERA-5 name
    print(fline)
    current_ERA_5_map = int(currentLine[61:65])#current ERA-5 map number
    ERA_5_wind_speed = int(currentLine[88:90]) #wind speed
    ERA_5_wind_direction = int(currentLine[92:96]) #wind direction
    if 8 <= ERA_5_wind_speed <= 10 and (300 <= ERA_5_wind_direction <= 359 or 0 <= ERA_5_wind_direction <= 30): #checking if the ERA-5 map fits the conditions
    #if current_ERA_5_time == 18:
    #if 1==1:
        for q in range(0,int(number_of_following_QuikSCAT_revs)): #going though all of the QuikSCAT files that follow that ERA-5 line

            QuikSCAT_line = l + q + 1 #determining what the QuikSCAT line number is
            #print('QuikSCAT rev on line: ' + str(QuikSCAT_line))
            currentLine = all_lines[QuikSCAT_line] #pulls current QuikSCAT line
            current_QuikSCAT_name = currentLine[0:99] #pulls QuikSCAT name
            print(current_QuikSCAT_name, q)
            try: #reads the QuikSCAT file
                nc_file = Dataset( current_QuikSCAT_name, 'r' )
                #print("file is ok")
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
                                    #if flags_Array[r,c] == 0:
                                    if 1==1:
                                        #print('r: ' + str(r) + ', c: ' + str(c))
                                        row_index, col_index = sub.Two_thousand_km_index_finder(lat_Array[r, c],long_Array[r, c]) #determining plot coordinates
                                        #print("Coordinate: (" + str(sub.truncate(lat_Array[r, c], 4)) + ", " + str(sub.truncate(long_Array[r, c], 4)) + ") is index: (" + str(row_index) + ", " + str(col_index) + ")") #just showing what index values the coordinates fall into
                                        try: #plotting wind speed. Has to be in try because of NaN values (that's what I found works, otherwise it throws a maskedArray error)
                                            if np.isnan(windSpeed_Array[r,c]) == False:
                                                plt_array[row_index, col_index] += windSpeed_Array[r,c] #assigning wind speed to plot element
                                                if windSpeed_Array[r,c] < min_speed:
                                                    min_speed = windSpeed_Array[r,c]
                                                if windSpeed_Array[r,c] > max_speed:
                                                    max_speed = windSpeed_Array[r,c]
                                                total_elements += 1
                                            #print(plt_array[row_index,col_index])
                                            if windSpeed_Array[r,c] != 0: #if the wind speed doesn't equal 0, add one to that spot in the dividing array
                                                #print('HIT DIVIDING ARRAY')

                                                dividing_array[row_index, col_index] += 1
                                        except:
                                            print("Out of range")
                                        #print()
                                        #print()

        QuikSCAT_revs_counted += 1 #add the number of QuikSCAT revs counted
        print('Number of QuikSCAT sets counted: ' + str(QuikSCAT_revs_counted)) #print it


print('Number of sets counted: ' + str(QuikSCAT_revs_counted))  # print it

output_file = '/Volumes/Blanken_HD/8_10_and_300_30_QuikSCAT_NEW_MASTER.txt'
read_output_file = open(output_file, 'w+')
#dividing array as mentioned when dividing array was initalized, currently commented out because of windSpeed_Array problems
dividing_value = 0
counter = 0

for r in range(0, 200):
    for c in range(0, 200):
        dividing_value = dividing_array[r,c]

        if dividing_value == 0:
            plt_array[r,c] = 0
            #print('No data @ ' + str(r) + ' ' + str(c))
        else:
            plt_array[r,c] /= dividing_value
        read_output_file.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array[r,c]) + '\n') #writes out [0:3] of row value, [4:7] col value and a guaranteed [8:16] of the wind speed
        counter += 1

        #print(r,c, plt_array[r,c])
read_output_file.close()
print("Average QuikSCAT speed: " + str(np.mean(plt_array)))
print("time: " + str(time.time()-start_time))
TNRfont = {'fontname':'Times New Roman'}
params = plt.rcParams
plot = plt.figure(figsize = (6.8,5.3), dpi=100)
plt.rcParams.update({'font.family': 'Times New Roman'})
plot_variable = plt.imshow(plt_array, extent = [long_coord_array[0], long_coord_array[199],lat_coord_array[199],lat_coord_array[0]], origin='upper',  cmap = 'gnuplot2',  vmax = 11.5)
plt.ylabel('latitude($^\circ$)', fontsize = 16, **TNRfont)
plt.xlabel('longitude($^\circ$)', fontsize = 16, **TNRfont)
plt.title(('QuikSCAT Data' + '\n' + '8-10 and 300-30 NEW MASTER FILE'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
print("Min speed: " + str(min_speed))
print("Max speed: " + str(max_speed))
print("Total elements: " +str(total_elements))
print('QuikSCAT Data' + '\n' + '8-10 and 300-30 NEW MASTER FILE')
cbar = plt.colorbar(plot_variable, fraction=0.05, pad=0.04)
cbarLabel = cbar.set_label('Wind speed (m/s)', fontsize = 16, **TNRfont)
plt.tick_params(axis='both', labelsize=16)
cbar.ax.tick_params(axis='y', labelsize=16)
bbox_props = dict(boxstyle="rarrow", fc=(1, 1, 1), ec="r", lw=0)
t = plt.text(500,750, "0 degrees", ha="center", va="center", rotation=0,size=15,bbox=bbox_props)
bb = t.get_bbox_patch()
bb.set_boxstyle("rarrow", pad=0.6)
#plt.savefig('QuikSCAT_Averaged_0_30.svg', dpi=100)
plt.show()
#My logic for when I started to wrtie this program

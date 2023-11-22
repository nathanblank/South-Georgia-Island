#This program outputs the characterstics of a wind shadow using ERA-5 data to determine upwind speed, but characteristics are only calculated based on shadows from directly behind the island.
#Refer to "QuikSCAT Wind Shadow Analyzer 2 MODES.py" for a few more detailed comments
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
corner_acc_speed = 0
corner_acc_element_counter = 0
wind_shadow_speed = 0
wind_shadow_element_counter = 0
short_shadows = 0
length_of_wind_shadow = 0
avg_length_of_wind_shadow = 0
number_of_wind_shadows_counted = 0
row_value_of_lowest_speed_in_last_column = 0
number_of_times_in_while = 0
last_ERA_5_name = ""
last_speed = 0
total_wind_shadows = 0
countable_wind_shadows = 0
exemption_wind_shadows = 0
small_wind_shadows = 0
large_wind_shadows = 0
problem_wind_shadows = 0
problem_revs = False
larger_than_speed_needed = 0
up_map_speed = 0
overall_upwind_ERA_5_speed = 0
overall_upwind_ERA_5_counter = 0
for l in range(0,len(all_lines)):
    print()
    print()
    print("Overall line: " + str(l))
    currentLine = all_lines[l] #pulls current line from master file
    number_of_following_QuikSCAT_revs = currentLine[0:1] #determines how many QuikSCAT revs follow
    if number_of_following_QuikSCAT_revs == '/': #if the line's first character is a '/', then it continues to the next line
        continue
    #print(number_of_following_QuikSCAT_revs, l) #otherwise it prints the number of following lines and line number

    fline = currentLine[2:60] #current ERA-5 name
    print(fline)
    current_ERA_5_map = int(currentLine[61:65])#current ERA-5 map number
    ERA_5_wind_speed = int(currentLine[88:90]) #wind speed
    ERA_5_wind_direction = int(currentLine[92:96]) #wind direction
    if 8 <= ERA_5_wind_speed <= 10 and (300 <= ERA_5_wind_direction <= 359 or 0 <= ERA_5_wind_direction <= 30): #checking if the ERA-5 map fits the conditions

        #print('objective 1')

        #ERA-5 upwind speed calcuations
        current_ERA_5_2000_km = np.zeros((200, 200), dtype='float') #setting up ERA-5 2000 km plot
        #METHOD NOT USED FOR UPWIND CALCULATION #map_counter_array = np.zeros((200, 200), dtype='float')  # used to count which elements in an ERA-5 map have wind speeds and which don't
        up_map_speed = 0 #initializing the upwind speed tracker
        if last_ERA_5_name == fline:  # checks to see if the file was already read or not
            print('File is same as before')
        else:
            print('File is different than before')
            nc_file = Dataset(fline, 'r')
            last_ERA_5_name = fline
            [attr_list, global_attr] = readnc.readGlobalAttrs(nc_file)
            [vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)
            latArray = var_data_list[1]  # ERA-lat array
            longArray = var_data_list[0]  # ERA-5 long array
            u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
            v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
        # 2000 km plot limits
        rowBegin = 541
        rowEnd = 613
        colBegin = 1230
        colEnd = 1353
        for r in range(rowBegin, rowEnd + 1):  # goes through all of the ERA-5 range that covers 2000 km plot
            for c in range(colBegin, colEnd + 1):
                row_index, col_index = sub.Two_thousand_km_index_finder(latArray[r],longArray[c])  # converts coordinate to 2000 km plot
                wind_speed = np.sqrt(u10[current_ERA_5_map, r, c] ** 2 + v10[current_ERA_5_map, r, c] ** 2)
                current_ERA_5_2000_km[row_index, col_index] = wind_speed  # establishes wind speeds on 2000 km plot
                #METHOD NOT USED FOR UPWIND CALCULATION #if wind_speed != 0:
                    #current_ERA_5_2000_km[row_index, col_index] = wind_speed  # establishes wind speeds on 2000 km plot
                    #map_counter_array[row_index, col_index] += 1
                #print(wind_speed)
        number_of_non_zero_ERA_5_up_wind_elements = 0
        #METHOD NOT USED FOR UPWIND CALCULATION #current_ERA_5_2000_km = sub.interp_era5(np.flipud(current_ERA_5_2000_km), np.flipud(map_counter_array)) #used to average the ERA-5 plot because of resolution differences from ERA-5 to 2000 km
        for r in range(90,110):
            for c in range(40,90):
                if current_ERA_5_2000_km[r,c] != 0: #checks for only ERA-5 elements that are non-zero. Some are 0 because of ERA-5 to 2000 km resolution change
                    up_map_speed += current_ERA_5_2000_km[r,c] #speed on the "upwind" side of island
                    number_of_non_zero_ERA_5_up_wind_elements += 1
                    overall_upwind_ERA_5_counter += 1
                    overall_upwind_ERA_5_speed += current_ERA_5_2000_km[r,c]
        up_map_speed /= number_of_non_zero_ERA_5_up_wind_elements
        #METHOD NOT USED FOR UPWIND CALCULATION #up_map_speed = np.mean(current_ERA_5_2000_km[0:200,0:90])
        print("Up map speed (based on ERA-5): " + str(up_map_speed))




        #QuikSCAT plotting and speed calculations
        RAW_current_revs = np.zeros((200, 200), dtype='float') #establishes array for 2000 km plot of RAW QuikSCAT data
        CALCULATED_current_revs = np.zeros((200, 200), dtype='float') #establishes the 2000 km plot for all revs for each ERA-5 time with the fixed 12.5 km resolution
        temp_dividing_array = np.zeros((200, 200),dtype='int')  # makes array which will be used to find average plot. The reason I have an array for this is because not all points in the plot get hit by every QuikSCAT rev, so when a point does get hit by one, it adds one to the dividing array at that point, and then the value at that point is used to later divide the sum of the speeds at that point

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
                                    if flags_Array[r,c] == 0:
                                        #print('r: ' + str(r) + ', c: ' + str(c))
                                        row_index, col_index = sub.Two_thousand_km_index_finder(lat_Array[r, c],long_Array[r, c]) #determining plot coordinates
                                        #print("Coordinate: (" + str(sub.truncate(lat_Array[r, c], 4)) + ", " + str(sub.truncate(long_Array[r, c], 4)) + ") is index: (" + str(row_index) + ", " + str(col_index) + ")") #just showing what index values the coordinates fall into
                                        try: #plotting wind speed. Has to be in try because of NaN values (that's what I found works, otherwise it throws a maskedArray error)
                                            if np.isnan(windSpeed_Array[r,c]) == False:
                                                plt_array[row_index, col_index] += windSpeed_Array[r,c] #assigning wind speed to plot element
                                                RAW_current_revs[row_index,col_index] += windSpeed_Array[r,c]


                                            #print(plt_array[row_index,col_index])
                                            if windSpeed_Array[r,c] != 0: #if the wind speed doesn't equal 0, add one to that spot in the dividing array
                                                #print('HIT DIVIDING ARRAY')
                                                temp_dividing_array[row_index,col_index] += 1
                                                dividing_array[row_index, col_index] += 1
                                        except:
                                            print("Out of range")
                                        #print()
                                        #print()
        temp_dividing_value = 0
        for r in range(0, 200):
            for c in range(0, 200):
                temp_dividing_value = temp_dividing_array[r, c]
                if temp_dividing_value == 0:
                    RAW_current_revs[r, c] = 0
                    # print('No data @ ' + str(r) + ' ' + str(c))
                else:
                    RAW_current_revs[r, c] /= temp_dividing_value

                # read_output_file.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array[r,c]) + '\n') #writes out [0:3] of row value, [4:7] col value and a guaranteed [8:16] of the wind speed
        CALCULATED_current_revs = np.copy(RAW_current_revs)

        for r in range (1,198):
            for c in range (1,198):
                if CALCULATED_current_revs[r, c] == 0.0:
                    if np.count_nonzero(RAW_current_revs[r - 1:r + 2, c - 1:c + 2]) == 0:
                        CALCULATED_current_revs[r, c] = 0.0
                    else:
                        CALCULATED_current_revs[r, c] = np.sum((RAW_current_revs[r - 1:r + 2, c - 1:c + 2])) / np.count_nonzero(RAW_current_revs[r - 1:r + 2, c - 1:c + 2])
        """
        for c in range(2,198):
            for r in range(2,198):
                if CALCULATED_current_revs[r,c] == 0.0 and np.sum(CALCULATED_current_revs[r-1:r+2, c+1]) != 0:
                    CALCULATED_current_revs[r,c] = np.sum((CALCULATED_current_revs[r-1:r+2,c-1:c+2])) / np.count_nonzero(CALCULATED_current_revs[r-1:r+2,c-1:c+2])
            c += 1

        for c in range(1,198):
            for r in range(1,198):
                if CALCULATED_current_revs[r,c] == 0.0 and np.sum(CALCULATED_current_revs[r-1:r+2, c+1]) != 0:
                    CALCULATED_current_revs[r,c] = np.sum((CALCULATED_current_revs[r-1:r+2,c-1:c+2])) / np.count_nonzero(CALCULATED_current_revs[r-1:r+2,c-1:c+2])
            c += 1
        """

        current_row = 99
        current_col = 109

        top_of_col = 0 #used to determine top row of each column
        bottom_of_col = 0 #used to determine bottom row of each column
        if np.any(CALCULATED_current_revs[current_row-5:current_row+6,current_col] <= (.9*up_map_speed)) == True and np.sum(CALCULATED_current_revs[94:104, current_col]) != 0.0:
            print("***************")
            print("WIND SHADOW PRESENT IN THIS SWATH")
            print('***************')
            countable_wind_shadows += 1
            total_wind_shadows += 1
            lowest_speed = 100
            lowest_r = 0
            for r in range(-5,6): #determines where start of wind shdaow is based on moving up and down 50 km each (100 km total)
                print(r,CALCULATED_current_revs[current_row+r,current_col], (.9*up_map_speed))

                if CALCULATED_current_revs[current_row+r,current_col] < lowest_speed and CALCULATED_current_revs[current_row+r, current_col] != 0.0:
                    lowest_speed = CALCULATED_current_revs[current_row+r,current_col]
                    lowest_r = r
            current_row = current_row + lowest_r
            print("Starting row: " + str(current_row))
            print("Starting col: " + str(current_col))
        else:
            print("NO VALID WIND SHADOW")
            for r in range(-5,6): #determines where start of wind shdaow is based on moving up and down 50 km each (100 km total)
                print(r,CALCULATED_current_revs[current_row+r,current_col], (.9*up_map_speed))
            larger_than_speed_needed += 1  
            total_wind_shadows += 1
            exemption_wind_shadows += 1
            continue
        lowest_speed_in_last_column = 100  # set at a large number to have the first point be automatically less

        while CALCULATED_current_revs[current_row, current_col] <= (up_map_speed*.9) and CALCULATED_current_revs[current_row,current_col] != 0.0 and current_row < 199 and current_row > 0 : #for each column
            print("HIT LOOP") #should print each time a new column starts

            print(current_row,current_col,(up_map_speed*.9), CALCULATED_current_revs[current_row, current_col])
            while CALCULATED_current_revs[current_row, current_col] <= (up_map_speed*.9) and CALCULATED_current_revs[current_row,current_col] != 0.0 and current_row < 199 and current_row > 0 : #loop for moving down in rows

                if CALCULATED_current_revs[current_row,current_col] < lowest_speed_in_last_column:
                    lowest_speed_in_last_column = CALCULATED_current_revs[current_row,current_col]
                    row_value_of_lowest_speed_in_last_column = current_row
                    print("LOWER WIND SPEED FOUND")
                print("Current row: " + str(current_row))
                print("Current col: " + str(current_col))
                print("Current wind speed: " + str(CALCULATED_current_revs[current_row, current_col]))
                print("Up map speed: " + str(up_map_speed * .9))
                print("Moving down")
                wind_shadow_speed += CALCULATED_current_revs[current_row, current_col]
                wind_shadow_element_counter += 1
                current_row += 1
            print("DONE MOVING DOWN")
            bottom_of_col = current_row - 1 #sets variable to tell where the last wind shadow element that was inside the wind shadow at bottom of that column

            current_row = row_value_of_lowest_speed_in_last_column #resetting row value to latest row

            while CALCULATED_current_revs[current_row, current_col] <= (up_map_speed*.9) and CALCULATED_current_revs[current_row,current_col] != 0.0 and current_row < 199 and current_row > 0 : #loop for moving up in rows

                print(current_row, current_col, CALCULATED_current_revs[current_row, current_col])

                if CALCULATED_current_revs[current_row,current_col] < lowest_speed_in_last_column:
                    lowest_speed_in_last_column = CALCULATED_current_revs[current_row,current_col]
                    row_value_of_lowest_speed_in_last_column = current_row
                    print("LOWER WIND SPEED FOUND")
                wind_shadow_speed += CALCULATED_current_revs[current_row, current_col]
                wind_shadow_element_counter += 1
                current_row -= 1
                print("Current row: " + str(current_row))
                print("Current col: " + str(current_col))
                print("Current wind speed: " + str(CALCULATED_current_revs[current_row,current_col]))
                print("Up map speed: " + str(up_map_speed*.9))
                print("Moving up")
            print("DONE MOVING UP")
            top_of_col = current_row + 1  # sets variable to tell where the last wind shadow element that was inside the wind shadow at top of that column

            if (bottom_of_col - top_of_col) < 4 and (current_col-109) > 3:
                print("WIND SHADOW LESS THAN 40 KM in N-S DIRECTION, WIND SHADOW CLOSED")
                short_shadows += 1
                continue
            current_col += 1 #moves to next column

            current_row = row_value_of_lowest_speed_in_last_column

            print("Next column")
            print("Current row: " + str(current_row))
            print("Current col: " + str(current_col))
            print("Current wind speed: " + str(CALCULATED_current_revs[current_row, current_col]))
            print("Up map speed: " + str(up_map_speed * .9))
        print("OUT OF WIND SHADOW ANALYSIS")

        length_of_wind_shadow = np.sqrt((((abs(current_row - 99))/lat_resolution)**2) + (((abs(current_col - 109))/long_resolution) ** 2))
        if (current_col - 109) == 1: #checks to see if wind shadow is small for characteristics sake
            small_wind_shadows += 1
        if length_of_wind_shadow > 0.0:
            avg_length_of_wind_shadow += length_of_wind_shadow
            number_of_wind_shadows_counted += 1
            print('Length of wind shadow: ' + str(length_of_wind_shadow) + ' km')
        if length_of_wind_shadow > 400:
            large_wind_shadows += 1


        #bottom corner acc determiner
        xstart = 103
        xend = 133
        ystart = 103
        yend = 133

        for r in range(ystart, yend):
            for c in range(xstart, xend):
                if (CALCULATED_current_revs[r, c] >= (up_map_speed*1.25)) and CALCULATED_current_revs[r,c] != 0.0: #checks to see if point is considered a corner acc
                    corner_acc_speed += CALCULATED_current_revs[r, c] #adds speed to counter
                    #print("Corner speed: " + str(current_rev[r,c]))
                    corner_acc_element_counter += 1 #adds to coorsponding counter

        #top corner acc determiner
        xstart = 97
        xend = 115
        ystart = 82
        yend = 98

        for r in range(ystart, yend):
            for c in range(xstart, xend):
                if (CALCULATED_current_revs[r, c] >= (up_map_speed * 1.25)) and CALCULATED_current_revs[r, c] != 0.0: #checks to see if point is considered a corner acc
                    corner_acc_speed += CALCULATED_current_revs[r, c]
                    # print("Corner speed: " + str(current_rev[r,c]))
                    corner_acc_element_counter += 1
        print()
        print()


        QuikSCAT_revs_counted += int(number_of_following_QuikSCAT_revs) #add the number of QuikSCAT revs counted
        print('Number of QuikSCAT revs counted: ' + str(QuikSCAT_revs_counted)) #print it
if number_of_wind_shadows_counted == 0:
    number_of_wind_shadows_counted += 1
overall_upwind_ERA_5_speed /= overall_upwind_ERA_5_counter
print("Average upwind wind speed: " + str(overall_upwind_ERA_5_speed))
print("Total wind shadows: " + str(total_wind_shadows))
print("Wind shadows that did not meet 40 km req: " + str(short_shadows))
print("Countable wind shadows: " + str(countable_wind_shadows))
print("Large wind shadows: " + str(large_wind_shadows))
print("Small wind shadows: " + str(small_wind_shadows))
print("Problem wind shadows: " + str(problem_wind_shadows))
print("Exemption wind shadows: " + str(exemption_wind_shadows))
print("Wind shadows with initial speeds larger than upwind reqs: " + str(larger_than_speed_needed))
print('Number of revs counted: ' + str(QuikSCAT_revs_counted))  # print it
avg_length_of_wind_shadow /= number_of_wind_shadows_counted
print("Number of wind shadows: " + str(number_of_wind_shadows_counted))
print('Wind shadow length = ' + str(avg_length_of_wind_shadow))
print('Total corner speed: ' + str(corner_acc_speed))
corner_acc_speed /= corner_acc_element_counter
print('Number of corner acceleration elements = ' + str(corner_acc_element_counter))
print('Corner acceleration speed = ' + str(corner_acc_speed))
wind_shadow_speed /= wind_shadow_element_counter
print('Number of wind shadow elements = ' + str(wind_shadow_element_counter))
print('Wind shadow speed = ' + str(wind_shadow_speed))

#output_file = '/Volumes/Blanken_HD/ALL_QuikSCAT.txt'
#read_output_file = open(output_file, 'w+')
#dividing array as mentioned when dividing array was initalized
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
        #read_output_file.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array[r,c]) + '\n') #writes out [0:3] of row value, [4:7] col value and a guaranteed [8:16] of the wind speed
        counter += 1

        #print(r,c, plt_array[r,c])
#read_output_file.close()
print("Average QuikSCAT speed: " + str(np.mean(plt_array)))
print("time: " + str(time.time()-start_time))
TNRfont = {'fontname':'Times New Roman'}
params = plt.rcParams
plot = plt.figure(figsize = (6.8,5.3), dpi=100)
plt.rcParams.update({'font.family': 'Times New Roman'})
plot_variable = plt.imshow(plt_array, extent = [long_coord_array[0], long_coord_array[199],lat_coord_array[199],lat_coord_array[0]], origin='upper',  cmap = 'gnuplot2', aspect= 1.5, vmin = 8.5, vmax = 11.5)
plt.ylabel('latitude($^\circ$)', fontsize = 16, **TNRfont)
plt.xlabel('longitude($^\circ$)', fontsize = 16, **TNRfont)
plt.title(('QuikSCAT data' + '\n' + '8-10 m/s and 300-30 degrees NEW DATA'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
print('QuikSCAT data' + '\n' + '8-10 m/s and 300-30 degrees NEW DATA')
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
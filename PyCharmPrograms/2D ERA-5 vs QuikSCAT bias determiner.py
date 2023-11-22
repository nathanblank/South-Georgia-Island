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


#ERA-5 is cols
#QuikSCAT is rows
QuikSCAT_MASK_array = np.zeros((200,200), dtype = "int")
QuikSCAT_data_array = np.zeros((200,200), dtype = "float")
ERA_5_data_array = np.zeros((200,200), dtype = "float")
plt_array = np.zeros((25, 25),dtype='int')
master_file_in = '/Volumes/Blanken_HD/Combined_ERA_5_and_QuikSCAT_Master_Version_2.txt' #master file pathname
read_master_file = open(master_file_in, 'r') #reads it
all_lines = read_master_file.readlines() #reads all lines
current_QuikSCAT_name = '' #initiates QuikSCAT name
current_ERA_5_name = '' #initiates ERA-5 name
ERA_5_wind_speed = 0 #initiates ERA-5 wind speed
ERA_5_wind_direction = 0 #initiates ERA-5 wind direction
QuikSCAT_ascending_point_value = 0 #initiates number of QuiKSCAT ascending points
QuikSCAT_descending_point_value = 0 #initiates number of QuikSCAT descening points

QuikSCAT_sets_counted = 0 #Counter to check how many QuikSCAT sets hit the condition
number_of_following_QuikSCAT_revs = 0 #number of revs after a certain ERA-5 map
last_ERA_5_name = " "
QuikSCAT_mean_upwind_speed = 0
ERA_5_mean_upwind_speed = 0
non_zero_ERA_5_elements = 0 #for the case when the QuikSCAT rev does not reach the upwind section of plot and forces an error
non_zero_QuikSCAT_elements = 0
bias_tracker = 0
bias_counter = 0
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




    #QuikSCAT plotting and speed calculations
    QuikSCAT_MASK_array = np.zeros((200, 200), dtype="int")
    QuikSCAT_data_array = np.zeros((200, 200), dtype="float")
    ERA_5_data_array = np.zeros((200, 200), dtype="float")
    temp_dividing_array = np.zeros((200, 200), dtype="float")
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
                                    row_index, col_index = sub.Two_thousand_km_index_finder(lat_Array[r, c],long_Array[r, c]) #determining plot coordinates
                                    try: #plotting wind speed. Has to be in try because of NaN values (that's what I found works, otherwise it throws a maskedArray error)
                                        if np.isnan(windSpeed_Array[r,c]) == False:
                                            QuikSCAT_data_array[row_index, col_index] += windSpeed_Array[r,c] #assigning wind speed to plot element
                                        if windSpeed_Array[r,c] != 0:
                                            temp_dividing_array[row_index,col_index] += 1
                                    except:
                                        print("Out of range")
                                    #print()
                                    #print()
    temp_dividing_value = 0
    for r in range(0, 200):
        for c in range(0, 200):
            temp_dividing_value = temp_dividing_array[r, c]
            if temp_dividing_value == 0:
                QuikSCAT_data_array[r, c] = 0
                # print('No data @ ' + str(r) + ' ' + str(c))
            else:
                QuikSCAT_data_array[r, c] /= temp_dividing_value
    for r in range(0,200):
        for c in range(0,200):
            if QuikSCAT_data_array[r,c] != 0:
                QuikSCAT_MASK_array[r,c] += 1


    # ERA-5 upwind speed calcuations
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
            row_index, col_index = sub.Two_thousand_km_index_finder(latArray[r], longArray[c])  # converts coordinate to 2000 km plot
            wind_speed = np.sqrt(u10[current_ERA_5_map, r, c] ** 2 + v10[current_ERA_5_map, r, c] ** 2)
            ERA_5_data_array[row_index, col_index] = wind_speed  # establishes wind speeds on 2000 km plot

    ERA_5_data_array *= QuikSCAT_MASK_array #makes sure that only ERA-5 elements are counted that have a cooresponding QuikSCAT are counted
    ERA_5_data_array = np.flipud(ERA_5_data_array)
    non_zero_QuikSCAT_elements = np.count_nonzero(QuikSCAT_data_array[0:200, 0:90])
    non_zero_ERA_5_elements = np.count_nonzero(ERA_5_data_array[0:200,0:90])
    if non_zero_QuikSCAT_elements == 0: #makes sure no errors are thrown
        non_zero_QuikSCAT_elements = 1
    if non_zero_ERA_5_elements == 0:
        non_zero_ERA_5_elements = 1

    ERA_5_mean_upwind_speed = int(np.sum(ERA_5_data_array[0:200, 0:90]) / non_zero_ERA_5_elements)  # computes average ERA-5 upwind speed
    QuikSCAT_mean_upwind_speed = int(np.sum(QuikSCAT_data_array[0:200, 0:90]) / non_zero_QuikSCAT_elements)
    print("ERA-5 upwind speed: " + str(ERA_5_mean_upwind_speed))
    print("QuikSCAT upwind speed: " + str(QuikSCAT_mean_upwind_speed))
    plt_array[ERA_5_mean_upwind_speed,QuikSCAT_mean_upwind_speed] += 1
    QuikSCAT_sets_counted += 1 #add the number of QuikSCAT sets counted
    print('Number of QuikSCAT revs counted: ' + str(QuikSCAT_sets_counted)) #print it


print('Number of QuikSCAT revs counted: ' + str(QuikSCAT_sets_counted)) #print it
output_file = '/Volumes/Blanken_HD/2D_ERA_5_vs_QuikSCAT_bias_determiner.txt'
read_output_file = open(output_file, 'w+')

for r in range(0, 25):
    for c in range(0, 25):
        read_output_file.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array[r,c]) + '\n') #writes out [0:3] of row value, [4:7] col value and a guaranteed [8:16] of the wind speed


        print(r,c, plt_array[r,c])
read_output_file.close()
plot_variable = plt.imshow(plt_array, origin='lower', aspect= 1.0, cmap = 'binary')
cbar = plt.colorbar(plot_variable, fraction=0.026, pad=0.04)
cbarLabel = cbar.set_label('Number of Maps')
cbar.ax.tick_params(axis='y', labelsize=16)
plt.xlabel("QuikSCAT average upwind speed (m/s)")
plt.ylabel("ERA-5 average upwind speed (m/s)")
plt.title("2D ERA-5 vs QuikSCAT bias determiner")
plt.show()
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


#ERA-5 is cols
#QuikSCAT is rows
QuikSCAT_MASK_array = np.zeros((200,200), dtype = "int")
QuikSCAT_data_array = np.zeros((200,200), dtype = "float")
ERA_5_data_array = np.zeros((200,200), dtype = "float")
plt_array = np.zeros((25, 25),dtype='int')
master_file_in = '/Volumes/Blanken_HD/Combined_ERA_5_and_QuikSCAT_Master_Version_2.txt' #master file pathname
read_master_file = open(master_file_in, 'r') #reads it
all_lines = read_master_file.readlines() #reads all lines
current_QuikSCAT_name = '' #initiates QuikSCAT name
current_ERA_5_name = '' #initiates ERA-5 name
ERA_5_wind_speed = 0 #initiates ERA-5 wind speed
ERA_5_wind_direction = 0 #initiates ERA-5 wind direction
QuikSCAT_ascending_point_value = 0 #initiates number of QuiKSCAT ascending points
QuikSCAT_descending_point_value = 0 #initiates number of QuikSCAT descening points

QuikSCAT_sets_counted = 0 #Counter to check how many QuikSCAT sets hit the condition
number_of_following_QuikSCAT_revs = 0 #number of revs after a certain ERA-5 map
last_ERA_5_name = " "
QuikSCAT_mean_upwind_speed = 0
ERA_5_mean_upwind_speed = 0
non_zero_ERA_5_elements = 0 #for the case when the QuikSCAT rev does not reach the upwind section of plot and forces an error
non_zero_QuikSCAT_elements = 0
bias_tracker = 0
bias_counter = 0
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




    #QuikSCAT plotting and speed calculations
    QuikSCAT_MASK_array = np.zeros((200, 200), dtype="int")
    QuikSCAT_data_array = np.zeros((200, 200), dtype="float")
    ERA_5_data_array = np.zeros((200, 200), dtype="float")
    temp_dividing_array = np.zeros((200, 200), dtype="float")
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
                                    row_index, col_index = sub.Two_thousand_km_index_finder(lat_Array[r, c],long_Array[r, c]) #determining plot coordinates
                                    try: #plotting wind speed. Has to be in try because of NaN values (that's what I found works, otherwise it throws a maskedArray error)
                                        if np.isnan(windSpeed_Array[r,c]) == False:
                                            QuikSCAT_data_array[row_index, col_index] += windSpeed_Array[r,c] #assigning wind speed to plot element
                                        if windSpeed_Array[r,c] != 0:
                                            temp_dividing_array[row_index,col_index] += 1
                                    except:
                                        print("Out of range")
                                    #print()
                                    #print()
    temp_dividing_value = 0
    for r in range(0, 200):
        for c in range(0, 200):
            temp_dividing_value = temp_dividing_array[r, c]
            if temp_dividing_value == 0:
                QuikSCAT_data_array[r, c] = 0
                # print('No data @ ' + str(r) + ' ' + str(c))
            else:
                QuikSCAT_data_array[r, c] /= temp_dividing_value
    for r in range(0,200):
        for c in range(0,200):
            if QuikSCAT_data_array[r,c] != 0:
                QuikSCAT_MASK_array[r,c] += 1


    # ERA-5 upwind speed calcuations
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
            row_index, col_index = sub.Two_thousand_km_index_finder(latArray[r], longArray[c])  # converts coordinate to 2000 km plot
            wind_speed = np.sqrt(u10[current_ERA_5_map, r, c] ** 2 + v10[current_ERA_5_map, r, c] ** 2)
            ERA_5_data_array[row_index, col_index] = wind_speed  # establishes wind speeds on 2000 km plot

    ERA_5_data_array *= QuikSCAT_MASK_array #makes sure that only ERA-5 elements are counted that have a cooresponding QuikSCAT are counted
    ERA_5_data_array = np.flipud(ERA_5_data_array)
    non_zero_QuikSCAT_elements = np.count_nonzero(QuikSCAT_data_array[0:200, 0:90])
    non_zero_ERA_5_elements = np.count_nonzero(ERA_5_data_array[0:200,0:90])
    if non_zero_QuikSCAT_elements == 0: #makes sure no errors are thrown
        non_zero_QuikSCAT_elements = 1
    if non_zero_ERA_5_elements == 0:
        non_zero_ERA_5_elements = 1

    ERA_5_mean_upwind_speed = int(np.sum(ERA_5_data_array[0:200, 0:90]) / non_zero_ERA_5_elements)  # computes average ERA-5 upwind speed
    QuikSCAT_mean_upwind_speed = int(np.sum(QuikSCAT_data_array[0:200, 0:90]) / non_zero_QuikSCAT_elements)
    print("ERA-5 upwind speed: " + str(ERA_5_mean_upwind_speed))
    print("QuikSCAT upwind speed: " + str(QuikSCAT_mean_upwind_speed))
    plt_array[ERA_5_mean_upwind_speed,QuikSCAT_mean_upwind_speed] += 1
    QuikSCAT_sets_counted += 1 #add the number of QuikSCAT sets counted
    print('Number of QuikSCAT revs counted: ' + str(QuikSCAT_sets_counted)) #print it


print('Number of QuikSCAT revs counted: ' + str(QuikSCAT_sets_counted)) #print it
output_file = '/Volumes/Blanken_HD/2D_ERA_5_vs_QuikSCAT_bias_determiner.txt'
read_output_file = open(output_file, 'w+')

for r in range(0, 25):
    for c in range(0, 25):
        read_output_file.write(str(r).zfill(3) + ' ' + str(c).zfill(3) + ' ' + str(plt_array[r,c]) + '\n') #writes out [0:3] of row value, [4:7] col value and a guaranteed [8:16] of the wind speed


        print(r,c, plt_array[r,c])
read_output_file.close()
plot_variable = plt.imshow(plt_array, origin='lower', aspect= 1.0, cmap = 'binary')
cbar = plt.colorbar(plot_variable, fraction=0.026, pad=0.04)
cbarLabel = cbar.set_label('Number of Maps')
cbar.ax.tick_params(axis='y', labelsize=16)
plt.xlabel("QuikSCAT average upwind speed (m/s)")
plt.ylabel("ERA-5 average upwind speed (m/s)")
plt.title("2D ERA-5 vs QuikSCAT bias determiner")
plt.show()

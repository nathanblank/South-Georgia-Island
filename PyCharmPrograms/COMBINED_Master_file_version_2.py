#The purpose of this program is to combine an ERA-5 master file and a QuikSCAT master file, interlacing the QuikSCAT revs with the ERA-5 maps.
#This program is supposed to output a text file that has a number of proceeding QuikSCAT revs that fall over South Georgia Island within a 3 hour range of when the ERA-5 map was created.
#After the number, an ERA-5 absoulte pathname is printed on the same line [2:61], then the map number of that ERA-5 file [62:66], then a date and time [67:86], then an average wind speed [88:90], then an average wind direction [92:96]
#The proceeding lines then consist of a varying number of QuikSCAT lines depending on how many fall in that specified ERA-5 map
#A QuikSCAT line has the following layout, QuikSCAT absolute path name [0:99], number of ascending path points [100:106] and decending number of points [106:113]
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
import datetime
from datetime import date, datetime, timedelta


# time it from here
start_time = time.time()

QuikSCAT_in = '/Volumes/Blanken_HD/REDUCED_master_file_2_0.txt' #The QuikSCAT master file

ERA_5_in = '/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_mnspd_mndir_MASTER_NEW.txt' #ERA-5 master file
Combined_master_output = '/Volumes/Blanken_HD/Combined_ERA_5_and_QuikSCAT_Master_Version_2_NEW.txt' #Output file
Read_output_master = open(Combined_master_output, 'w') #Read version of combined master file

QuikSCAT_master_read = open(QuikSCAT_in, 'r') #read QuikSCAT master file
ERA_5_master_read = open(ERA_5_in, 'r') #read ERA-5 master file
print("files are ok")

all_QuikSCAT_lines = QuikSCAT_master_read.readlines() #gets all lines in QuikSCAT master file
all_ERA_5_lines = ERA_5_master_read.readlines() #gets all lines in ERA-5 master file

#prints length of each of the master files
print(len(all_ERA_5_lines))
print(len(all_QuikSCAT_lines))


QuikSCAT_line_number = 0 #initializes line 0 for counting through ERA-5 files
QuikSCAT_writing_array = ['1', '2', '3', '4'] #makes array for absolute QuikSCAT path names to be written into

hour_diff_in_QuikSCAT_and_ERA_5 = 3 #sets the initial difference in hours to be  3 so that the program goes into the while loop
time_of_QuikSCAT_file = 0 #initializes the QuikSCAT time variable
current_ERA_5_line = 'NNN' #absolute pathname of current ERA-5 file

line_counter = 0 #counts difference in lines when going through QuikSCAT files

for l in range(1, len(all_ERA_5_lines)): #for loop going through all ERA-5 files minus the first one because it is irrelevant
    print('Time: ' + str(time.time() - start_time))
    print('Percent: ' + str((l*100/len(all_ERA_5_lines))))
    writing_array_element = 0 #setting the QuikSCAT writing array element to 0
    QuikSCAT_writing_array = ['1', '2', '3', '4']  # makes array for absolute QuikSCAT path names to be written into
    while hour_diff_in_QuikSCAT_and_ERA_5 <= 3.0:
        current_ERA_5_line = all_ERA_5_lines[l] #grabs the current ERA-5 line (pathname, time, etc.)
        current_ERA_5_time = current_ERA_5_line[65:84] #pulls out the time
        current_QuikSCAT_line = all_QuikSCAT_lines[QuikSCAT_line_number] #pulls current QuikSCAT line
        current_QuikSCAT_file = current_QuikSCAT_line[0:99] #grabs current QuikSCAT absolute pathname
        read_current_QuikSCAT_file = Dataset(current_QuikSCAT_file, 'r') #reads that QuikSCAT file

        #unpacking QuikSCAT file
        [attr_list, global_attr] = readnc.readGlobalAttrs(read_current_QuikSCAT_file)
        [vars, var_attr_list, var_data_list] = readnc.readVars(read_current_QuikSCAT_file)

        #initalizing arrays
        time_Array = var_data_list[0]
        lat_Array = var_data_list[1]
        long_Array = var_data_list[2]
        windSpeed_Array = var_data_list[3]
        windDirection_Array = var_data_list[4]
        rain_Array = var_data_list[5]
        flags_Array = var_data_list[6]

        # used to determine where the satelitte goes over SGI so that way an accurate time can be determined
        if int(current_QuikSCAT_line[100:106]) > 0:
            # ascending QuikSCAT limits
            rowBegin = 237
            rowEnd = 425
            colBegin = 0
            colEnd = 152
        else:
            # descending QuikSCAT limits
            rowBegin = 2823
            rowEnd = 3011
            colBegin = 0
            colEnd = 152

        time_of_QuikSCAT_file = time_Array[int((rowEnd+rowBegin)/2)] #takes average of latitude from SGI region depending on ascending or descending rev
        newDTBegin = timedelta(np.float64(time_of_QuikSCAT_file/(24*3600))) #converts seconds to a date and time
        adjusted_QuikSCAT_time = datetime(1999, 1,1) + newDTBegin #adds starting reference point
        time_of_QuikSCAT_file = sub.hour_rounder(adjusted_QuikSCAT_time) #rounds to the nearest hour
        print('Time of ERA-5 file is: ' + str(current_ERA_5_time))
        print("Time of QuikSCAT file is: " + str(time_of_QuikSCAT_file))
        datetimeFormat = '%Y-%m-%d %H:%M:%S%f' #Formats date and time to be able to find difference into ERA-5 and QuikSCAT times
        hour_diff_in_QuikSCAT_and_ERA_5 = abs(datetime.strptime(str(current_ERA_5_time), datetimeFormat) - datetime.strptime(str(time_of_QuikSCAT_file), datetimeFormat)).total_seconds() / 3600. #finds difference in time and divides by 3600 to convert from seconds to hours
        print('Hour difference between ERA-5 and QuikSCAT: ' + str(hour_diff_in_QuikSCAT_and_ERA_5))

        if hour_diff_in_QuikSCAT_and_ERA_5 <= 3.0: #checks to see if it found a QuikSCAT time that matches with an ERA-5 time
            QuikSCAT_writing_array[writing_array_element] = str(current_QuikSCAT_line) #saves that absolute pathname to the array for later writing
            writing_array_element += 1 #moves variable to next element position
            print('hit')
            QuikSCAT_line_number += 1 #moves to next QuikSCAT file to check against same ERA-5 file


    #when the while loop no longer proves to be true
    if writing_array_element > 0:
        print(QuikSCAT_writing_array) #makes sure that array is correct
        print('**************')
        print('STARTING WRITING')
        Read_output_master.write(str(writing_array_element) + ' ' + str(current_ERA_5_line))  # write the current ERA-5 line
        print('QuikSCAT rev counter: ' + str(writing_array_element))
        for e in range(0, writing_array_element): #go through all of the elements that have stuff in them
            Read_output_master.write(QuikSCAT_writing_array[e]) #write them
        print('DONE WRITING')
        print('**************')
    hour_diff_in_QuikSCAT_and_ERA_5 = 1 #makes sure that the program goes back into while loop upon new ERA-5 line
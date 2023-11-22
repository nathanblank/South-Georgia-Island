#This program determines the number of QuikSCAT revs that fall under certain ERA-5 conditions.
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
QuikSCAT_revs_counted = 0 #Counter to check how many QuikSCAT revs hit the condition
number_of_following_QuikSCAT_revs = 0 #number of revs after a certain ERA-5 map


start_speed = 8
end_speed = 10
start_direction1 = 300
end_direction1 = 359
start_direction2 = 0
end_direction2 = 30


for l in range(0, len(all_lines)): #going through however many number of lines (first QuikSCAT rev on line 18)
    currentLine = all_lines[l] #pulls current line from master file
    number_of_following_QuikSCAT_revs = currentLine[0:1] #determines how many QuikSCAT revs follow
    if number_of_following_QuikSCAT_revs == '/': #if the line's first character is a '/', then it continues to the next line
        continue

    current_ERA_5_name = currentLine[2:60] #current ERA-5 name
    currentMapSpeed = int(currentLine[88:90]) #wind speed
    currentMapDirection = int(currentLine[92:96]) #wind direction
    if start_speed <= currentMapSpeed <= end_speed and (start_direction1 <= currentMapDirection <= end_direction1 or start_direction2 <= currentMapDirection <= end_direction2):
        QuikSCAT_revs_counted += int(number_of_following_QuikSCAT_revs) #add the number of QuikSCAT revs counted
        print(QuikSCAT_revs_counted) #print it


print("Number of QuikSCAT revs that meet conditions " +str(start_speed) + '-' + str(end_speed) + ' ' + str(start_direction1) + '-' + str(end_direction1) + ' and ' + str(start_direction2) + '-' + str(end_direction2) + ' = ' + str(QuikSCAT_revs_counted))

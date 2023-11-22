#This program creates a file that shows the percent of accepted wind shadows for each month for every year for QuikSCAT data.
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



master_file_in = '/Volumes/Blanken_HD/Accepted_vs_exemption_shadows_300_30.txt' #master file pathname
read_master_file = open(master_file_in, 'r') #reads it
written_file_out = '/Volumes/Blanken_HD/ANALYZED_Accepted_vs_exemption_shadows_300_30.txt'
read_written_file_out = open(written_file_out, 'w+')
all_lines = read_master_file.readlines() #reads all lines
currentLine = all_lines[0]

accepted_revs_array = np.zeros((12, 10), dtype = 'int')
total_revs_array = np.zeros((12, 10), dtype = 'int')
for l in range(0, len(all_lines)):
    currentLine = all_lines[l]
    current_time = str(currentLine[11:19])
    current_day = int(currentLine[8:10])
    current_month = int(currentLine[5:7])
    current_year = int(currentLine[3:4])
    print(current_time, current_day, current_month,2000 + current_year, int(currentLine[20]))
    if int(currentLine[20]) == 1:
        accepted_revs_array[current_month-1,current_year] += 1
        total_revs_array[current_month-1,current_year] += 1
    else:
        total_revs_array[current_month-1,current_year] += 1

for r in range(0,10):
    for c in range(0,12):
        print(c+1,2000+r,accepted_revs_array[c,r],total_revs_array[c,r],100*float(accepted_revs_array[c,r]/total_revs_array[c,r]))
        read_written_file_out.write('200' + str(r) + "-" + str(c+1) + ' ' + str(100*float(accepted_revs_array[c,r]/total_revs_array[c,r])) + '\n' )


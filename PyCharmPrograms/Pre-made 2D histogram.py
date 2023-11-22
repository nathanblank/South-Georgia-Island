import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
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
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import matplotlib as matplotlib



# time it from here
start_time = time.time()


#ERA-5 is cols
#QuikSCAT is rows

plt_array = np.zeros((25, 25),dtype='int')
axis_array = np.zeros(25, dtype=int)
for r in range(0,25):
    axis_array[r]=r
master_file_in = '/Volumes/Blanken_HD/2D_ERA_5_vs_QuikSCAT_bias_determiner.txt' #master file pathname
read_master_file = open(master_file_in, 'r') #reads it
all_lines = read_master_file.readlines() #reads all lines
total_sets_of_QuikSCAT = 0
for l in range(0,len(all_lines)):
    currentLine = all_lines[l]
    r_value = int(currentLine[0:3])
    c_calue = int(currentLine[4:7])
    value_value = int(currentLine[8:12])
    total_sets_of_QuikSCAT += value_value
    if value_value == 0 or value_value>2000:
        value_value = 1
    print(r_value, c_calue, value_value)
    plt_array[r_value,c_calue] = value_value
print("Total number of QuikSCAT realizations: " + str(total_sets_of_QuikSCAT))
plot_variable = plt.contourf(plt_array,1000, extent = [0,20,0,20],origin='lower', cmap = 'hot')
#plot_variable = plt.imshow(plt_array,origin='lower', aspect= 1.0,extent = [0,20,0,20],aspect= 1.0,cmap = 'hot')
#plt.plot([0,20],[0,20])
cbar = plt.colorbar(plot_variable, fraction=0.026, pad=0.04)
cbarLabel = cbar.set_label('Number of Maps/Revs')
cbar.ax.tick_params(axis='y', labelsize=16)
plt.xlabel("QuikSCAT average upwind speed (m/s)")
plt.ylabel("ERA-5 average upwind speed (m/s)")
plt.title("2D ERA-5 vs QuikSCAT bias determiner")
plt.show()

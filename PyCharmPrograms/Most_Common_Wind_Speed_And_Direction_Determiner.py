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
import os.path
from netCDF4 import Dataset
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib


#time and date is range char [60,79]
#wind speed is range [86,88]
#wind direction is range [90,93]

master_file = '/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_mnspd_mndir_MASTER.txt'

speedIndexMax = 20
meanArraySD = np.zeros((speedIndexMax,36), dtype = int)
inline = open(master_file, 'r')
line = inline.readlines()

mapCounter = 0
for l in range (0,14612):
    currentLine = line[l]
    if currentLine == 'END':
        break
    currentSpeed = currentLine[86:88]
    currentSpeedIndex = int(int(currentSpeed))
    currentDir = int(currentLine[90:93])
    currentDirIndex = int(currentDir/10)
    meanArraySD[currentSpeedIndex, currentDirIndex] += 1
    print(currentSpeedIndex,currentDirIndex)
    if 8 <= currentSpeedIndex <= 10 and (300 <= int(currentDir) <= 359 or 0 <= int(currentDir) <= 30):
        mapCounter += 1
print(mapCounter)
#meanArraySD[8, 33] = 0
#meanArraySD[9, 34] = 0

#for s in range(8,11):
   # for d in range (0,36):
     #   if

from mpl_toolkits.axes_grid1 import make_axes_locatable
print('Number of maps in condition: ' + str(mapCounter))
TNRfont = {'fontname':'Times New Roman'}
plot = plt.figure(figsize = (8.1,4.4), dpi=100)
plot_variable = plt.contourf(meanArraySD, origin='lower', aspect= 1.0, cmap = 'winter', extent=[18,35,0,20])
plt.tick_params(axis='both', labelsize=16)
plt.title(('ERA-5 Mean Speeds and Directions'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
plt.xlabel('Mean Wind Direction (10 degrees)', fontsize = 16, **TNRfont)
plt.ylabel('Mean Wind Speed (m/s)', fontsize = 16, **TNRfont)





cbar = plt.colorbar(plot_variable, fraction=0.026, pad=0.04)
cbarLabel = cbar.set_label('Number of Maps', fontsize = 16, **TNRfont)
cbar.ax.tick_params(axis='y', labelsize=16)
plt.savefig('Most_Common.svg', dpi=100)

for s in range (0,speedIndexMax): #pr
    print('Maps at ' + str(s) + ' m/s: ' + str(np.sum(meanArraySD[s,:])))
plt.show()


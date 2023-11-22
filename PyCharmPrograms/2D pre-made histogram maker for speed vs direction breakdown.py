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
from matplotlib.colors import LogNorm

#time and date is range char [60,79]
#wind speed is range [86,88]
#wind direction is range [90,93]

master_file = '/Volumes/Blanken_HD/South Georgia Project/ERA5_mnspd_mndir_data_pulled.txt'

speedIndexMax = 20
meanArraySD = np.zeros((speedIndexMax,36), dtype = "float")
inline = open(master_file, 'r')
line = inline.readlines()
dir_array = np.zeros(36,dtype='int')
spd_array = np.zeros(speedIndexMax,dtype="int")
for r in range(0,speedIndexMax):
    spd_array[r] = r
for r in range(0,36):
    dir_array[r] = r*10 - 180
mapCounter = 0
total_maps = 0
for l in range (0,14612):
    currentLine = line[l]
    total_maps += 1
    if currentLine == 'END':
        break
    currentSpeed = int(currentLine[0:2])
    currentSpeedIndex = currentSpeed
    currentDir = int(currentLine[2:5])
    currentDirIndex = int(currentDir)
    if currentDir >= 18:
        currentDirIndex -= 18
    else:
        currentDirIndex += 18
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

#Accounts for making a percentage of each cross-section. (divided by 14612 maps, multiplied by 100 for percent)
meanArraySD /= 146.12

from mpl_toolkits.axes_grid1 import make_axes_locatable
print('Number of maps in condition: ' + str(mapCounter))
print("Total number of maps: " + str(total_maps))
print("Percent of maps condition takes: " + str(float(100*mapCounter/total_maps)))
TNRfont = {'fontname':'Times New Roman'}
plot = plt.figure(figsize = (8.1,4.4), dpi=100)
plot_variable = plt.imshow(meanArraySD, origin='lower', extent = [dir_array[0],dir_array[35], spd_array[0],spd_array[19]], aspect = 18, cmap = 'seismic')
#plt.plot([-30,-30,30,30,-30],[8,10,10,8,8], 'g',lineWidth = 2)
plt.tick_params(axis='both', labelsize=16)
plt.title(('ERA-5 Mean Speeds and Directions'), fontdict=None, loc='center', pad=None, fontsize = 32, **TNRfont)
plt.xlabel('Mean Wind Direction (degrees)', fontsize = 16, **TNRfont)
plt.ylabel('Mean Wind Speed (m/s)', fontsize = 16, **TNRfont)





cbar = plt.colorbar(plot_variable, fraction=0.026, pad=0.04)
cbarLabel = cbar.set_label('Percent of Maps', fontsize = 16, **TNRfont)
cbar.ax.tick_params(axis='y', labelsize=16)
plt.savefig('Most_Common.svg', dpi=100)

for s in range (0,speedIndexMax): #pr
    print('Maps at ' + str(s) + ' m/s: ' + str(np.sum(meanArraySD[s,:])))
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from optparse import OptionParser
import readnc
import sys
import time
import MandNsubs as sub
import array as arr
import matplotlib.axes as ax

from netCDF4 import Dataset
import mysubs as ms   # get the file with all of my subroutines

import matplotlib.pyplot as plt
import matplotlib as matplotlib

lat_resolution = 0.09 #degrees
long_resolution = 0.2 #degrees

plt_array = np.zeros((200,200), dtype=float) #initiates plot array
lat_coord_array = np.zeros(200, dtype=float) #initiates latitude values
long_coord_array = np.zeros(200, dtype=float) #initiates longitude values

coordinate_row = -45.3 #top left corner lat value
coordinate_col = -17.1 #top left corner long value
counter = 0
for r in range (0,200):
    for c in range(0,200):
        lat_coord_array[r] = coordinate_row
        long_coord_array[c] = coordinate_col
        row_index, col_index = sub.Near_Zero_Two_thousand_km_index_finder(coordinate_row,coordinate_col)
        print(r,c)
        print("Coordinate: (" + str(sub.truncate(coordinate_row, 4)) + ", " + str(sub.truncate(coordinate_col, 4)) + ") is index: (" + str(row_index) + ", " + str(col_index) + ")")
        coordinate_col -= long_resolution
        #plt_array[r,c] = counter
        #counter += 1
    coordinate_row -= lat_resolution
    coordinate_col = -17.1  # resets the initial row value for the next col
plt_array[100, 100] = 1 # shows the center of the plot (SGI)
plt.imshow(plt_array, extent = [long_coord_array[199], long_coord_array[0],lat_coord_array[199],lat_coord_array[0]], origin='upper',  cmap = 'nipy_spectral', aspect=2.0)
plt.ylabel('latitude($^\circ$)')
plt.xlabel('longitude($^\circ$)')
plt.title(('2000 km x 2000 km Plot Centered Over SGI with 10 km Resolution'), fontdict=None, loc='center', pad=None)
plt.colorbar()
plt.show()
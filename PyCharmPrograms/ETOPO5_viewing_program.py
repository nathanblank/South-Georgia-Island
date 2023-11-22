import numpy as np  #instead of writing "numpy." just use "np."
import pandas as pd
from optparse import OptionParser
import readnc
import MandNsubs as sub
from netCDF4 import Dataset
import os.path
import matplotlib.pyplot as plt

# put in filename here, should be a string of form [].nc
# ncfile = 'qs_l2b_18415_v3.1_200301011347.nc'
ncfile = '/Volumes/Macintosh HD/Users/N-Dogg/Downloads/SRT IV/ETOPO5/ETOPO5.nc'  # this is the ETOPO5 data file

# From ncwrapper.py, but edited by me to work with python 3
# all print statements now have parenthesis,
# and due to differences with how odicts work I had to change the print vars[i] bit.

# authorship
__author__     = "David Moroni"
__copyright__  = "Copyright 2012, California Institute of Technology"
__credits__    = ["Ed Armstrong and David Moroni"]
__license__    = "none"
__version__    = "1.0"
__maintainer__ = "David Moroni"
__email__      = "david.m.moroni at jpl dot nasa dot gov"
__status__     = "Release Candidate"

completeName = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/SGI_and_falklands_in_ETOPO5.txt')

SGI_in_ETOPO5 = open(completeName, "w+")
try:
    nc_file = Dataset( ncfile, 'r' )
    print("file is ok")
except IOError:
    print('not a valid netCDF file')
print(nc_file)
print('Global attributes')
[attr_list, global_attr] = readnc.readGlobalAttrs( nc_file )
natts = len(attr_list)
#for n in range(0, natts):
#     print(attr_list[n]," = ",global_attr[n])

# --------------------------------------------------
# read and print variables and their attributes
# --------------------------------------------------
#print('----------')
#print('Variables:' )
[vars, var_attr_list, var_data_list] = readnc.readVars( nc_file )
nvars = len(vars)
#print('Number of variables = ', nvars)
for i in range(0, nvars):
    vardata = var_data_list[i]
#    print('----------')
#    print(var_attr_list[i])
#    print(list(vars)[i], '[0:10] =\n', vardata[0:10]) # changed by me

# close the file
nc_file.close()

rowBegin= 340
rowEnd = 460
colBegin = 3750
colEnd = 3950

#copy the data arrays to be sure that we don't inadvertantly change them
lon_arr=np.copy(var_data_list[0])
lat_arr=np.copy(var_data_list[1])
elev_arr=np.copy(var_data_list[2])
lon_arr2 = lon_arr[rowBegin:rowEnd]
lat_arr2 = lat_arr[colBegin:colEnd]
elev_arr2 = elev_arr[rowBegin:rowEnd, colBegin:colEnd]
nlons=len(lon_arr)
nlats=len(lat_arr)
print('nlats=',nlats,'  nlons=',nlons)

#print(lat_arr[0:100])

# make an input elevation array that is 1 for land (any positive elevations), 0 for ocean (any 0 or negative elevation)
elev_arr_binary = np.copy(elev_arr)
elev_arr_binary[np.where(elev_arr > 0)] = 1.
elev_arr_binary[np.where(elev_arr <= 0)] = 0.

#plot the binary elevation array
sub.ETOPO5_five_coordinate_finder(2000,2000) #test
sub.ETOPO5_index_finder(-90,180) #test
elev_arr_binary2 = np.flipud(elev_arr_binary)
#elev_arr_binary3 = np.fliplr(elev_arr_binary2)
counter = 0 #counts how many ETOPO5 boxes SGI takes up (51)
for r in range(rowBegin,rowEnd):
    for c in range(colBegin,colEnd):
        if elev_arr_binary2[r,c] == 1: #if land
            row_coord, col_coord = sub.ETOPO5_five_coordinate_finder(r,c) #run subroutine
            row_coord = np.negative(float(row_coord)) #make it negative because SGI is below the equator
            row_coord = "{0:.4f}".format(row_coord) #format string
            col_coord = 360 - float(col_coord) #put coordinate into correct format
            col_coord = "{0:.4f}".format(col_coord) #format string
            SGI_in_ETOPO5.write(str(row_coord) + ' ' + str(col_coord) +  '\r\n') #write into text file
            counter += 1
print("Counter = " + str(counter))
SGI_in_ETOPO5.close()

plt.matshow(elev_arr_binary2, origin = 'lower', cmap='binary')  # cmap sets the color bar - you can get colormap names from matplotlib.org/users/colormaps.html
#, extent = [lon_arr[colBegin],lon_arr[colEnd],lat_arr[rowEnd],lat_arr[rowBegin]]
plt.show()






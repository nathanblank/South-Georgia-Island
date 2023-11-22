#This program outputs text files with the date/time of an ERA-5 map and then the average wind speed and direction on that map over the SGI region.
# The text file it is put into is based on the map's wind speed and direction.
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

#  A prog to investigate the structure of the ERA5 u10/v10 files downloaded from Copernicus
# based on netcdf read code from census_8a.py



# time it from here
start_time = time.time()
def characteristicsOutputter(file_extension,inputMapBegin,y,m):
    #fline = '/Volumes/Satellite_Data/ERA5_downloads/2001_01_uv.nc'     # This is a sample absolute address
    #fline = '/Users/N-Dogg/Downloads/SRT IV/ECMWF_ERA5_Analyses/2001_01_uv.nc'
    fline = file_extension
    # now read the ERA5 file and close it
    ncfile = fline
    nc_file = Dataset(ncfile, 'r')
    nc_file.close()
    #Date and time for plot
    import datetime
    from datetime import date, timedelta, datetime

    [attr_list, global_attr] = readnc.readGlobalAttrs(nc_file)
    [vars, var_attr_list, var_data_list] = readnc.readVars(nc_file)
    #need to convert time/date input into map numbers

    mapNumBegin = inputMapBegin #mapNumBegin is the map number you're looking at
    mapNumEnd = 0

    #used to determine how many maps based on number of days in the month.
    if m == 2 and y % 4 == 0: #leap year february - 29 days
        mapNumEnd = 115

    if m == 2 and y % 4 != 0: #non leap year february - 28 days
        mapNumEnd = 111

    if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:  #months with 31 days
        mapNumEnd = 123

    if m == 4 or m == 6 or m == 9 or m == 11:  #months with 30 days
        mapNumEnd = 119

    print(m)
    print(mapNumEnd)

    u10 = var_data_list[3]  # 10 m height zonal (east-west) wind component speed, m/s
    v10 = var_data_list[4]  # 10 m height meridional (north-south) wind component speed, m/s
    w10 = var_data_list[2]  # time for each data map
    def timeDateDeterminer(currentMapNumber):
        w10_pltCurrent = w10[currentMapNumber]  # used to determine beginning time
        daysChange = w10_pltCurrent / 24.
        #print(daysChange)
        newDTCurrent = timedelta(np.float64(daysChange))
        print(newDTCurrent)
        dtCurrent = datetime(1900, 1, 1) + newDTCurrent
        dtCurrent = dtCurrent.replace(y,m)

        return str(dtCurrent)

    #ERA-5 plot limits
    rowBegin= 523
    rowEnd = 610
    colBegin = 1198
    colEnd = 1378
    #World map limits
    #rowBegin= 0
    #rowEnd = 720
    #colBegin = 0
    #colEnd = 1439
    start_time = time.time() #determines starting time

    #ERA5_characteristics.write('File name: ' + fline + '\r\n')
    #print(completeName)
    #from here down are goal numbers 2 and 3, plot the data within the ERA5 box

    #w10_pltEnd = w10[mapNumEnd] # used to determine end time


    #these lines are greyed out so i don't know that they are needed
    u10_plt = u10[mapNumBegin, :,:]  # defines u10_plt
    v10_plt = v10[mapNumBegin, :,:] # defines v10_plt
    mapNumLoopVar = 0 #will be used to count how many coordinate points are being looked at.
    umean = 0.
    vmean = 0.


    for h in range(mapNumBegin, mapNumEnd+1):
        currentDateTime = timeDateDeterminer(h)
        print('Map num: ' + str(h))
        map_spd = np.sqrt(u10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2 + v10[h,rowBegin:rowEnd+1,colBegin:colEnd+1]**2) #determines map speed over all of the maps that it looks through
        map_spd_average = np.mean(map_spd)
        umean = np.mean(u10[h,rowBegin:rowEnd + 1, colBegin:colEnd + 1])
        vmean = np.mean(v10[h,rowBegin:rowEnd + 1, colBegin:colEnd + 1])
        dirmean = np.rad2deg(np.arctan2(vmean,umean)) #vector mean calculation in degrees
        print('Map date & time: ' + currentDateTime)
        print('Map speed: ' + str(map_spd_average))
        print('Map direction: ' + str(dirmean))

        #The if statements look to see if the map in question is within the certain wind speed and wind direction in degrees
        if map_spd_average < 3:
            ERA5_1to3.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average < 3 and dirmean >= -45 and dirmean < 45:
            ERA5_1to3E.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average < 3 and dirmean >= 45 and dirmean < 135:
            ERA5_1to3N.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average < 3 and dirmean >= 135 and dirmean < -135:
            ERA5_1to3.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average < 3 and dirmean >= -135 and dirmean < -45:
            ERA5_1to3.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')

        if map_spd_average >= 3 and map_spd_average < 5:
            ERA5_3to5.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 3 and map_spd_average < 5 and dirmean >= -45 and dirmean < 45:
            ERA5_3to5E.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 3 and map_spd_average < 5 and dirmean >= 45 and dirmean < 135:
            ERA5_3to5N.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 3 and map_spd_average < 5 and dirmean >= 135 and dirmean < -135:
            ERA5_3to5W.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 3 and map_spd_average < 5 and dirmean >= -135 and dirmean < -45:
            ERA5_3to5S.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')

        if map_spd_average >= 5 and map_spd_average < 7:
            ERA5_5to7.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 5 and map_spd_average < 7 and dirmean >= -45 and dirmean < 45:
            ERA5_5to7E.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 5 and map_spd_average < 7 and dirmean >= 45 and dirmean < 135:
            ERA5_5to7N.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 5 and map_spd_average < 7 and dirmean >= 135 and dirmean < -135:
            ERA5_5to7W.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 5 and map_spd_average < 7 and dirmean >= -135 and dirmean < -45:
            ERA5_5to7S.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')

        if map_spd_average >= 7 and map_spd_average < 9:
            ERA5_7to9.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 7 and map_spd_average < 9 and dirmean >= -45 and dirmean < 45:
            ERA5_7to9E.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 7 and map_spd_average < 9 and dirmean >= 45 and dirmean < 135:
            ERA5_7to9N.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 7 and map_spd_average < 9 and dirmean >= 135 and dirmean < -135:
            ERA5_7to9W.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 7 and map_spd_average < 9 and dirmean >= -135 and dirmean < -45:
            ERA5_7to9S.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')

        if map_spd_average >= 9:
            ERA5_9andAbove.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 9 and dirmean >= -45 and dirmean < 45:
            ERA5_9andAboveE.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 9 and dirmean >= 45 and dirmean < 135:
            ERA5_9andAboveN.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 9 and dirmean >= 135 and dirmean < -135:
            ERA5_9andAboveW.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')
        if map_spd_average >= 9 and dirmean >= -135 and dirmean < -45:
            ERA5_9andAboveS.write(currentDateTime + ', ' + str(np.mean(map_spd)) + ', ' + str(dirmean) + '\r\n')

        #ERA5_characteristics.write(currentDateTime + ', '+ str(np.mean(map_spd)) + '\r\n')
        #u10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += u10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
        #v10_plt[rowBegin:rowEnd+1, colBegin:colEnd+1] += v10[h, rowBegin:rowEnd+1,colBegin:colEnd+1]
        #u10_plt = u10_plt / (mapNumEnd - (mapNumBegin-1))
        #v10_plt = v10_plt / (mapNumEnd - (mapNumBegin-1))
    #ERA5_characteristics.close()
    #print(map_spd.shape)
    """
    atmp = map_spd
    tmp_mean = np.mean(atmp)


    # note that var_data_list[2] is a 1-D array of MAP TIMES, var_data_list[1] is a 1-D array of LATITUDES for each map,
    #         and var_data_list[0] is a 1-D array of LONGITUDES for each map
    
    longArray = var_data_list[0]
    latArray = var_data_list[1]
    print()
    print()
    print("Average wind speed is: ", tmp_mean, " m/s")

    
    

    print()

    # determines end time for output
    daysChange = w10_pltEnd / 24
    print(daysChange)
    newDTEnd = timedelta(np.float64(w10_pltEnd / 24.))
    dtEnd = datetime(1900, 1, 1) + newDTEnd
    print(newDTEnd)
    print('Date of map ends at', dtEnd)
    print(w10_pltEnd, ' end hours after Jan 1, 1900 is:', dtEnd)
    #plt.matshow(atmp, cmap='jet')
    aatmp = np.flipud(atmp)
    #aatmp = np.fliplr(aatmp)
    fig = plt.figure()

    #ax1 = fig.add_subplot(211)
    #ax1.set_ylabel('longitude(degrees)')
    #ax1.set_xlabel('latitude(degrees)')
    plt.xlabel('latitude($^\circ$)')
    plt.ylabel('longitude($^\circ$)')
    

    #ax.Axes(aatmp, [0,0,0,0], facecolor=None, frameon=True, sharex=None, sharey=None, label='latitude', xscale=None, yscale=None, **kwargs)
    #plt.imshow(aatmp, extent = [longArray[colBegin], longArray[colEnd], latArray[rowEnd], latArray[rowBegin]], origin='lower', aspect= 2.0)
    #matplotlib.axis.Axes.set_label_text('latitude(', 'u\u00b0', ')')
    #matplotlib.axes.Axes.set_xlabel(self, 'latitude(', 'u\u00b0', ')',labelpad=None, **kwargs)

    #plt.contour(aatmp, origin = 'lower',extent = [longArray[colEnd], longArray[colBegin], latArray[rowEnd], latArray[rowBegin]], linewidths = 1) #makes resolution more "flowy" and not "pixely"
    #Y, X = np.mgrid[0:4320:100j, 0:2160:100j]
    #plt.streamplot(X, Y, u10_plt, v10_plt) #shows arrows, might be good for speed and direction
    #x = longitude
    #y = latitude

    #plt.title(('Average Wind Speeds From ' + str(dtBegin) +' to '+ str(dtEnd) + ' in m/s'), fontdict=None, loc='center', pad=None)
    #plt.axis([-60,-40, 360, 300])
    cbar = plt.colorbar() #shows wind speed bar from blue to red
    cbarLabel = cbar.set_label('Wind speed (m/s)')
    

    #plt.show()
    plt.savefig(fname = 'ERA5map' + str(mapNumBegin)+ '.png')
    print()
    """
#establishes variables for each of the files
completeName1to3 = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_1to3.txt')
completeName1to3N = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_1to3N.txt')
completeName1to3S = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_1to3S.txt')
completeName1to3E = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_1to3E.txt')
completeName1to3W = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_1to3W.txt')

completeName3to5 = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_3to5.txt')
completeName3to5N = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_3to5N.txt')
completeName3to5S = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_3to5S.txt')
completeName3to5E = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_3to5E.txt')
completeName3to5W = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_3to5W.txt')

completeName5to7 = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_5to7.txt')
completeName5to7N = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_5to7N.txt')
completeName5to7S = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_5to7S.txt')
completeName5to7E = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_5to7E.txt')
completeName5to7W = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_5to7W.txt')

completeName7to9 = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_7to9.txt')
completeName7to9N = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_7to9N.txt')
completeName7to9S = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_7to9S.txt')
completeName7to9E = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_7to9E.txt')
completeName7to9W = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5__7to9W.txt')

completeName9andAbove = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_9andAbove.txt')
completeName9andAboveN = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_9andAboveN.txt')
completeName9andAboveS = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_9andAboveS.txt')
completeName9andAboveE = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_9andAboveE.txt')
completeName9andAboveW = os.path.join('/Volumes/Blanken_HD/ERA5_Output_Data/ERA5_wind_9andAboveW.txt')

file_name = '/Volumes/Blanken_HD/ERA5_Data/ERA5_downloads/2000_01_uv.nc'  # initial condition for file name

#These lines open all of the files
ERA5_1to3 = open(completeName1to3, "w+")
ERA5_1to3W = open(completeName1to3W, "w+")
ERA5_1to3N = open(completeName1to3N, "w+")
ERA5_1to3E = open(completeName1to3E, "w+")
ERA5_1to3S = open(completeName1to3S, "w+")

ERA5_3to5 = open(completeName3to5, "w+")
ERA5_3to5W = open(completeName3to5W, "w+")
ERA5_3to5E = open(completeName3to5E, "w+")
ERA5_3to5N = open(completeName3to5N, "w+")
ERA5_3to5S = open(completeName3to5S, "w+")

ERA5_5to7 = open(completeName5to7, "w+")
ERA5_5to7S = open(completeName5to7S, "w+")
ERA5_5to7N = open(completeName5to7N, "w+")
ERA5_5to7E = open(completeName5to7E, "w+")
ERA5_5to7W = open(completeName5to7W, "w+")

ERA5_7to9 = open(completeName7to9, "w+")
ERA5_7to9N = open(completeName7to9N, "w+")
ERA5_7to9S = open(completeName7to9S, "w+")
ERA5_7to9E = open(completeName7to9E, "w+")
ERA5_7to9W = open(completeName7to9W, "w+")

ERA5_9andAbove = open(completeName9andAbove, "w+")
ERA5_9andAboveN = open(completeName9andAboveN, "w+")
ERA5_9andAboveS = open(completeName9andAboveS, "w+")
ERA5_9andAboveE = open(completeName9andAboveE, "w+")
ERA5_9andAboveW = open(completeName9andAboveW, "w+")

for y in range (2001,2002): # sets the year
    for m in range (1,10): # sets the month
        print(m)
        file_name = '/Volumes/Blanken_HD/ERA5_Data/ERA5_downloads/' + str(y) + '_0' + str(m) + '_uv.nc'  # sets file path for months 1-9
        print(file_name) #prints file name to make sure output dates align with month being calculated
        characteristicsOutputter((file_name),0,y,m) #calls main method to do calculations
        print('Time elapsed: ' + str(time.time() - start_time)) #keeps track of how long it takes to do one month
    for m in range(10,13):  # sets the month
        print(m)
        file_name = '/Volumes/Blanken_HD/ERA5_Data/ERA5_downloads/' + str(y) + '_' + str(m) + '_uv.nc'  # sets file path for months 10-12
        print(file_name)  # prints file name to make sure output dates align with month being calculated
        characteristicsOutputter((file_name), 0, y, m)  # calls main method to do calculations
        print('Time elapsed: ' + str(time.time() - start_time))  # keeps track of how long it takes to do one month

#These lines add up number of occurrences for each type of general speed and direction
ERA5_1to3.write('Times of occurrence: ' + str(len(open(completeName1to3).readlines())))
ERA5_1to3W.write('Times of occurrence: ' + str(len(open(completeName1to3W).readlines())))
ERA5_1to3N.write('Times of occurrence: ' + str(len(open(completeName1to3N).readlines())))
ERA5_1to3E.write('Times of occurrence: ' + str(len(open(completeName1to3E).readlines())))
ERA5_1to3S.write('Times of occurrence: ' + str(len(open(completeName1to3S).readlines())))

ERA5_3to5.write('Times of occurrence: ' + str(len(open(completeName1to3).readlines())))
ERA5_3to5W.write('Times of occurrence: ' + str(len(open(completeName3to5W).readlines())))
ERA5_3to5E.write('Times of occurrence: ' + str(len(open(completeName3to5E).readlines())))
ERA5_3to5N.write('Times of occurrence: ' + str(len(open(completeName3to5N).readlines())))
ERA5_3to5S.write('Times of occurrence: ' + str(len(open(completeName3to5S).readlines())))

ERA5_5to7.write('Times of occurrence: ' + str(len(open(completeName5to7).readlines())))
ERA5_5to7S.write('Times of occurrence: ' + str(len(open(completeName5to7S).readlines())))
ERA5_5to7N.write('Times of occurrence: ' + str(len(open(completeName5to7N).readlines())))
ERA5_5to7E.write('Times of occurrence: ' + str(len(open(completeName5to7E).readlines())))
ERA5_5to7W.write('Times of occurrence: ' + str(len(open(completeName5to7W).readlines())))

ERA5_7to9.write('Times of occurrence: ' + str(len(open(completeName7to9).readlines())))
ERA5_7to9N.write('Times of occurrence: ' + str(len(open(completeName7to9N).readlines())))
ERA5_7to9S.write('Times of occurrence: ' + str(len(open(completeName7to9S).readlines())))
ERA5_7to9E.write('Times of occurrence: ' + str(len(open(completeName7to9E).readlines())))
ERA5_7to9W.write('Times of occurrence: ' + str(len(open(completeName7to9W).readlines())))

ERA5_9andAbove.write('Times of occurrence: ' + str(len(open(completeName9andAbove).readlines())))
ERA5_9andAboveN.write('Times of occurrence: ' + str(len(open(completeName9andAboveN).readlines())))
ERA5_9andAboveS.write('Times of occurrence: ' + str(len(open(completeName9andAboveS).readlines())))
ERA5_9andAboveE.write('Times of occurrence: ' + str(len(open(completeName9andAboveE).readlines())))
ERA5_9andAboveW.write('Times of occurrence: ' + str(len(open(completeName9andAboveW).readlines())))

#These lines close all of the files
ERA5_1to3.close()
ERA5_1to3W.close()
ERA5_1to3N.close()
ERA5_1to3E.close()
ERA5_1to3S.close()

ERA5_3to5.close()
ERA5_3to5W.close()
ERA5_3to5E.close()
ERA5_3to5N.close()
ERA5_3to5S.close()

ERA5_5to7.close()
ERA5_5to7S.close()
ERA5_5to7N.close()
ERA5_5to7E.close()
ERA5_5to7W.close()

ERA5_7to9.close()
ERA5_7to9N.close()
ERA5_7to9S.close()
ERA5_7to9E.close()
ERA5_7to9W.close()

ERA5_9andAbove.close()
ERA5_9andAboveN.close()
ERA5_9andAboveS.close()
ERA5_9andAboveE.close()
ERA5_9andAboveW.close()
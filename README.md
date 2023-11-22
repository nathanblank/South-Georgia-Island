# South-Georgia-Island

This repository covers the data science project I worked on in high school. I worked  with Dr. Michael Freilich to analyze 10 years (over 4 TB) of satellite and weather model data to determine wind patterns around South Georgia Island.

Link to final presentation: https://dfba632ed2.clvaw-cdnwnd.com/dd903f77cf34fa450440cfbaada6362d/200000126-d7722d7723/blanken_nathan.pptx?ph=dfba632ed2


FILE INFORMATION--------------------------------------------------------
THESE ARE NOTES FOR COMMONLY OCCURRING CASES FOR THE SOUTH GEORGIA ISLAND PROJECT THAT TOOK PLACE BETWEEN JUNE 2019 AND MAY 2020 BY Nathan Blanken AND Michael Freilich.




NEW/REFINED VERSUS ORIGINAL ANALYSIS

Any data files that say "NEW" or "REFINED", should be considered to have been created based on refined ERA-5 plot zoning. This means that the average conditions for the ERA-5 maps were from a 500 km (long) by 200 km (lat) region directly west of the island. If the file does not say "NEW" or "REFINED", assume the ERA-5 averages for each map was calculated based on the entire 2000 km region. 


CONFIRMED CASES

Any text file that has "CONFIRMED" at the end of it indicates that the text file was looked over to verify that data was not written over by other conditions, wind speeds, wind directions, etc.





PRE-MADE TEXT FILES

For any .txt files that have some form of:

000 000 ###########
000 001 ###########
000 002 ###########

These files are most likely able to be read in by a program that has the word pre-made in it. It will most likely be "Pre-made 2000 km viewer.py". Those text files are formatted in this way:

rrr ccc speed/direction
rrr ccc speed/direction
rrr ccc speed/direction


Any programs that write into a file in the for:

For r in range(0,###):
	for c in range(0,###):
		______________

Will output the file in the format mentioned directly above.







Brief description of each program


2D ERA-5 vs QuikSCAT bias determiner.py - Creates a line graph of all ERA-5 and QuikSCAT elements and plots percent of elements at each speed for each data source.

2D pre-made histogram maker for speed vs direction breakdown.py - Creates 2D histogram showing breakdown of ERA-5 mean speed and direction cross sections.

10km plot.py - Program creating a blank 10 km resolution plot. This was the basis for the 2000 km plot.

Accepted and Exemption plot maker NO ERA-5.py - Plot that makes the accepted and exemption plots for QuikSCAT data. The plots are created based on a preset upwind speed (change numerator of "up_map_speed" variable to change upwind wind speed)

Accepted and Exemption Wind Shadow plot maker YES ERA-5.py - Same as above program but ERA-5 is used to calculate upwind wind speed

Accepted versus Exemption time line maker.py - Creates a text file that can be imported into excel that shows each time and date when a set of QuikSCAT revs either had an accepted shadow or an exempted shadow. This was used to determine if there was any seasonal correlation to when shadows were produced. 

Both 1D speed histograms.py - This program creates a 1D histogram plotting both the ERA-5 and QuikSCAT percent of elements at each wind speed on the y-axis and the actual wind speeds on the x-axis. 

COMBINED_Master_file_version_2.py - Creates a combined master file for both ERA-5 and QuikSCAT, matching the maps and revs together based on time. 

Conditional_data_spd_plt_visualizer.py - First generation pre-made viewing program. This is not necessarily important as it was used in the early stages of the project, but more advanced programs now do the same thing.

Conditional_Wind_Speed_Averager.py - Creates a conditional climatology plot of ERA-5 data from one condition, plots it and writes it.

Conditional_Wind_Speed_Averager_Many_Outputs_2.0.py - Creates conditional climatology plots of ERA-5 data for three different speeds or directions, plots them in one figure, and writes all of the results to a text file. 

Corner acceleration determiner.py - Determines just the southern corner acceleration in an ERA-5 or QuikSCAT conditional climatology plot, not from individual realizations.

ERA5_master_file_generator_type2.py - Creates ERA-5 master file. Outputs a text file with each ERA-5 absolute path name, map number, date and time, as the average speed and direction of that map over the area that is being averaged (I.e. 500 km by 200 km (refined) or entire map (original analysis)).

ERA5_one_map_visualizer.py - Can show one ERA-5 map from any particular file and any particular map.

ERA5MapNumberDeterminer.py - Determines map number from an ERA-5 file based on time.

ERA-5 conditional map counter.py - Counts the number of ERA-5 maps that meet a specified condition.

ERA-5 element by element plot maker.py - Creates a 1D histogram showing the breakdown in the number of points that hit each wind speed from ERA-5 data.

ERA-5 1D plot maker for Wind Direction.py - Creates a line graph showing break down of percent of elements that hit each wind direction for ERA-5 data.

ERA_5 Conditional Averager 2000 km plot.py - Creates conditional climatology plots for ERA-5 data.

ERA_5_and_QuikSCAT_Combined_Master_File_Generator.py - Creates combined master file based on similar times for ERA-5 and QuikSCAT.

ETOPO5_viewing_program.py - Displays ETOP05.

line_counter.py - Counts the number of lines in a text file

M&Nsubs.py - Secondary subroutine python program.

MandNsubs.py - Main subroutine python program. (Should include all subroutines in M&Nsubs.py)

Most_Common_Wind_Speed_And_Direction_Determiner.py - One program that creates the 2D histogram of the ERA-5 mean wind speed and wind direction breakdown. Refer to "2D pre-made histogram maker for speed vs direction breakdown.py" for clearer results.

mysubs.py - Old subroutine program. Kept just in case.

mysubs copy.py - Old subroutine program. Kept just in case.

Pre-made histogram viewer DIRECTION.py - Plots data from a pre-calculated text file including the percent of each wind direction from ERA-5, not very important.

Pre-made 1D histogram viewer.py - Can do same as program above, it can also do ERA-5 and QiukSCAT wind speeds from pre-calculated text file.

Pre-made 2D histogram.py - Creates a 2D histogram showing bias between ERA-5 and QuikSCAT wind speeds.

pre-made 2000 km plot maker TWO DATA SETS TEST.py - Finds the difference of pre-calculated 2000 km plots.

Pre-made 2000 km viewer.py - THE MOST IMPORTANT PROGRAM FOR PLOTTING PRE-CALCULATED 2000 KM PLOTS.

QuikSCAT Conditional Averager.py - This program creates conditional climatology plots for varying wind speeds and wind directions and write the 200 element by 200 element into a text file for future use.

QuikSCAT conditional map counter.py - This program determines the number of QuikSCAT revs that fall under certain ERA-5 conditions.

QuikSCAT rev timeline analysis.py - This program creates a file that shows the percent of accepted wind shadows for each month for every year for QuikSCAT data.

QuikSCAT viewer V2.py - This program makes a plot of a single QuikSCAT rev over the SGI region.

QuikSCAT Wind Shadow Analyzer.py - This program outputs the characterstics of a wind shadow using ERA-5 data to determine upwind speed, but characteristics are only calculated based on shadows from directly behind the island. Refer to "QuikSCAT Wind Shadow Analyzer 2 MODES.py" for a few more detailed comments.

QuikSCAT Wind Shadow Analyzer 2 MODES.py - This program outputs characteristics of a wind shadow using the 2 mode method (directly behind island and then some distance down wind). It uses ERA-5 to calculate the average upwind speed, not a set constant.

QuikSCAT Wind Shadow averager NO ERA-5.py - This program will spit out characteristics of the wind shadow and corner accelerations based on a preset value "up_wind_speed"

QuikSCAT 1D histogram element counter.py - This program creates a 1D plot of the number of the speed of elements from all of the QuikSCAT revs that hit inside the SGI region.

QuikSCAT_master_file_reducer.py - This program creates a text file that outputs the file path of the QuikSCAT rev as well as how many points hit inside the SGI region. The first section of numbers is how many points hit if the rev was an ascending rev and the second set is for if it was a descending rev.

QuiKSCAT_number_of_points_Determiner.py - This program makes a 1D histogram of the number of points that each QuikSCAT rev has when it goes over the SGI region.

QuiKSCAT_percent_of_points_Determiner.py - This program makes a 1D histogram of the percent of points that each QuikSCAT rev has when it goes over the SGI region.

readnc.py - "Blackbox" for unpacking .nc files.

Wind_Direction_Averager2.0.py - This program plots the average direction at each element over the SGI region based on a specified range of ERA-5 maps.

Wind_Speed_Averager_HUMAN_One_Map.py - This program allows the user to put in a date and time, selects that map, and then creates plot of that map. The time must be in the range of the input file.

Wind_Speed_Averager_HUMAN_Two_Maps.py - This program allows the user to put in two separate dates and times, selects those maps, and then creates an average plot from them. Both times must be in the range of the input file.

Wind_Speed_Averager_Multiple_Files_speed_and_direction_separated.py - This program outputs text files with the date/time of an ERA-5 map and then the average wind speed and direction on that map over the SGI region. The text file it is put into is based on the map's wind speed and direction.

Wind_Speed_Averager_Multiple_Files_speed_separated.py - This program outputs text files with the date/time of an ERA-5 map and then the average wind speed on that map over the SGI region. The text file it is put into is based on the map's wind speed.


Wind_Speed_Averager_Simple9.0.py - This program takes in a month of ERA-5 maps and then can average any range of maps within that range.


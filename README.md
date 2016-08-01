    ##########################################################
    #     Licensed under GPL/GNU - free software license     #
    #                                                        #
    #   You may share/distribute/commercially use as you     #
    #      see fit. I only ask that you give me credit       #
    #      when applicable. Thanks.                          #
    #                                                        #
    #               Created by: Duan Uys                     #
    ##########################################################


# Geophysics - Gravity Data Reduction #

This is a program that inputs a simple data file and
spits out the corrected gravity measurements appended to 
original data.

Gravity Corrections Included:

* Drift Correction
* Latitude Correction
* Free-air Correction
* Bouguer Correction

You will need 3 files for this program to work, and they must all be in the same directory as the main program file
called 'grav'

Files Needed:

* grav (grav.exe - windows)
* config.txt
* data.txt


### DATA.TXT ###
This file will contain the raw gravity data along with other important positional, elevation, and time data.
It is organised into 4 columns separated by whitespace.

        **SAMPLE**
        #x   y   g_record(mGal)  time_elapsed(min)  height_to_base (metres)
        
        1	 -5	     7362.725        16.5	            79.92
        2	 -25	 7362.825        26.73	            79.89
        3	 -30	 7362.83         34.1               79.92
        4	 -35	 7362.87         44.53	            79.92
        5	 -40	 7362.865        48.867	            79.96


--> the file containing the data can be renamed to anything. In the configuration file - more below - you have the option
  to specify the name of the file.

    ########## CONFIG.TXT ############
    --------------------------------------------------
    ## these are comments
    
    # name of data file - can be renamed to anything you want
    data_file = data.txt
    
    # name of output file - change name of output file or leave alone
    output_file = grav_corr.txt
    
    # in degrees
    latitude = -33.773
    
    # in kg/m^3
    avg_density = 2400
    
    # base 1 reading mGal
    base1 = 7362.64
    
    # base 2 reading mGal
    base2 = 7362.63
    
    # base height - metres
    base_height = 80
    
    # total time of survey - minutes
    total_time = 136




### HOW TO USE ###
#####<u>OS and Linux</u> ####

Simply have all three files in the same directory as explained above and execute 'grav' located in the OSX folder
in the terminal window like:

    ./grav
If anything goes wrong - the terminal should try to help tell you what went wrong and how to solve it.

#####<u>Windows</u> ####
Simply have all three files in the same directory as explained above and double-click:

    grav.exe
If anything goes wrong - the terminal should try to help tell you what went wrong and how to solve it.


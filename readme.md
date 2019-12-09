# HDF5 to GeoJSON Converter
This repository was done as part of my Computer Science and Engineering Masters at Instituto Superior Técnico titled: "Maretec Forecast Responsive Visualization".

## Description
The script in this repository was developed with the goal of converting HDF5 files to a format suitable for visualization using Javascript libraries. The target format GeoJSON allows us to have a standardized data structure to be visualized. This way the same data can be used across different visualizations.

## Project Files
* /converter/ - final files for the script
    * config.py - Settings file for the Script, here many aspects of the algorithm can be defined, include the input and output files.
    * converter.py - Algorithm Implementation, includes the AreaConverter for most magnitudes converted and vectorConverter for vector magnitudes. These functions are called by the main.py file. This structure helps the use of multi processing and/or threading.
    * domains.json - JSON file with the details of each domain, this file is essential and must follow the detailed structure.
    * magnitudes.json - JSON file with the configuration for each magnitude. These settings impact the execution of the script and should be refined as usage increases.
    * main.py - Main file where configurations are imported and the script is started. The multiprocessing part happens in this file.  
* /development/ - includes some intermediate steps taken during the development of the solution

## Script Configurations
The config.py file includes the general configurations of the script. The file includes a more precise documentation.

* CONF_MULTIPROCESSING - Use multiprocessing or not (recommended True)
* CONF_COORDINATEROUNDING - Decimal Places Rounding for coordinates (recommended 4 to 5)
* CONF_USESCALE - Use value mapping or not

* CONF_INPUTDATE - HDF5 Files to use as input
* CONF_DOMAIN - Name of the Domain to be computed (must be the same as in the HDF5 file)
* CONF_ALLTIMEFRAMES - Compute the 24 hours of the domain
* CONF_24HOURLIST - The 'name' of each timeframe dataset
* CONF_TIMEFRAME - Timeframe to be converted if ALLTIMEFRAMES is False
* CONF_MAGNITUDE - Magnitude to be convertif if MULTIPROCESSING is False
* CONF_VECTORSTEP - an X by X square is used to reduce the number of computed values in the vector Magnitudes (recommended 3 to 5)


### Magnitude Configurations
The magnitudes.json file includes the necessary configurations for each magnitude to be computed. If a magnitude is not present in this file, the script will fail to execute.

* name - Name of the magnitude
* hdfName - Name as used on the HDF file (use an array if you want to specify two datasets)
* outputName - Name that will be used on the output file (avoid special characters)
* maxValue - Upper limit of the scale for this magnitude (adjust this value as necessary)
* minValue - Lower limit of the scale for this magnitude (adjust this value as necessary)
* rounding - The number of decimal places to use in the calculations and output (adjust this value as necessary)
* unit - Unit of this magnitude
* formula - Unused field as of now, was included to accommodate the necessity of unit conversion
* vector - Is magnitude a vector magnitude? (eg: Temperature = true, Wind Direction = false)
* showTogether - Use when you want to display two magnitudes simultaneously (use 'name' for the companion)
* colorScale - Color Scale to be displayed with this magnitude, the number of steps is automatically adjusted by the script, you can use an array of either 2 steps or 20 (recommended maximum of 15 steps)

## Algorithm
A detailed description of the algorithm implemented can be found on this Dissertation documents. I recommend the Extended Abstract as a quicker way to understand it. Or instead read the comments along the code, they detail some of the most tricky aspects of the code. In there you may also find some bits of unused code that can be of interest to you. 
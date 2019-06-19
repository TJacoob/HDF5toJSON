# -- PROGRAM CONFIGURATIONS --

# Use multiprocessing ( True or False )
# Enables processing all the magnitudes available for the selected domain
CONF_MULTIPROCESSING = True

# Add domain information to the first object of the geojson feature list
CONF_ADDDOMAININFO = False

# How many decimal places are used to round coordinates ( should be 4 ou 5 )
CONF_COORDINATEROUNDING = 5

# Hide magnitude values, using a scale (check valueMapper function)
CONF_USESCALE = True
CONF_MAXSCALE = 20
CONF_MINSCALE = 0

# -- EXECUTION CONFIGURATIONS --

# Name of the HDF5 File to use as input
CONF_INPUTDATA = "../testFiles/WaterProperties_Surface.hdf5"
CONF_OUTPUTDATA = "../testFiles/test.json"  #UNUSED RIGHT NOW

# Domain to be computed
CONF_DOMAIN = "DOM_PCOMS"

# Time slot to compute ( 00001 to 00024 )
CONF_TIMEFRAME = "00001"

# If multiprocessing is turned off, select magnitude to be calculated
# Check magnitudes.py for options
CONF_MAGNITUDE = "TEMPERATURE"






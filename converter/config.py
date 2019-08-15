# -- PROGRAM CONFIGURATIONS --

# Use multiprocessing ( True or False )
# Enables processing all the magnitudes available for the selected domain
CONF_MULTIPROCESSING = True


# Add domain information to the first object of the geojson feature list
# Disabled for now
#CONF_ADDDOMAININFO = False

# How many decimal places are used to round coordinates ( should be 4 ou 5 )
CONF_COORDINATEROUNDING = 5

# Hide magnitude values, using a scale (check valueMapper function)
CONF_USESCALE = True
# Ununsed right now, uses the magnitude color scale instead
CONF_MAXSCALE = 10
CONF_MINSCALE = 0

# -- EXECUTION CONFIGURATIONS --

# Name of the HDF5 File to use as input
CONF_INPUTDATA = ["../testFiles/Hydrodynamic_Surface.hdf5","../testFiles/WaterProperties.hdf5"]
CONF_OUTPUTDATA = "../testFiles/test.json"  #UNUSED RIGHT NOW

# Domain to be computed
CONF_DOMAIN = "PCOMS"

# Compute all time frames for the domain
CONF_ALLTIMEFRAMES = False

# List of timeframes to use
# Might new two lists, for 24 hour range and 6 hour range, or a configuration field
CONF_24HOURLIST = ["00001","00002","00003","00004","00005","00006","00007","00008","00009","00010","00011","00012",
                   "00013","00014","00015","00016","00017","00018","00019","00020","00021","00022","00023","00024"]

# If single time slot, specify which one to compute ( 00001 to 00024 )
CONF_TIMEFRAME = "00001"

# If multiprocessing is turned off, select magnitude to be calculated
# Check magnitudes.py for options
CONF_MAGNITUDE = "VELOCITY"






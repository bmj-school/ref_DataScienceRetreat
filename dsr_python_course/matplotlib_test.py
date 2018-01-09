#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Standard modules
#===============================================================================

#===============================================================================
#--- SETUP external modules
#===============================================================================
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import openpyxl as openpyxl
import seaborn as sb

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.util_inspect import get_self

#===============================================================================
#--- MAIN CODE
#===============================================================================

#--- Set Pandas options
pd.set_option('display.height', 500)
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def run():
    #--- Get DFs, full and test
    #load_data()
    plt.figure()
    x = [1,2,3,4]
    y = [1,4,9,16]
    plt.plot(x,y)
    plt.show()
    
if __name__ == "__main__":
    
    run()
    print("Done")
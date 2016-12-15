
import os
import numpy as np
import glob
import pandas as pd
from netCDF4 import Dataset,netcdftime,num2date


files=glob.glob('data/raw/SPEI/CMIP5/*')

nc=Dataset('data/raw/SPEI/CMIP5/spei_hadgem2-es_rcp2.6_1950-2099_1m.nc')
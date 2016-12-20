
from netCDF4 import Dataset,netcdftime,num2date



def rename_netcdf(in_file,out_file,varname,varname_out):
	nc_in=Dataset(in_file,"r")
	print in_file
	nc_out=Dataset(out_file,"w")
	print out_file

	for dname, the_dim in nc_in.dimensions.iteritems():
		nc_out.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)

	# Copy variables
	for v_name, varin in nc_in.variables.iteritems():
		if v_name==varname:
			outVar = nc_out.createVariable(varname_out, varin.datatype, varin.dimensions)					    
			outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
			outVar[:] = varin[:]				

		else:	
			outVar = nc_out.createVariable(v_name, varin.datatype, varin.dimensions)					    
			outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
			outVar[:] = varin[:]

	# close the output file
	nc_out.close()
	nc_in.close()




import os
import numpy as np
import glob
import pandas as pd

files=glob.glob('/p/projects/tumble/carls/shared_folder/rx5/old/mon_rx5_1960-1999_*')
for file in files:
	rename_netcdf(file,file.replace('old/',''),'Rx5_monthly','rx5')

import numpy as np
from netCDF4 import Dataset
import os

def country_zoom(in_file,out_file,var,iso,mask_path='masks/'):
	'''
	compute weighted country average for each timestep
	in_file: type str: file to be processed
	out_file: type str: filepath where output is going to be stored
	var: type str: variable name in netcdf file
	iso: type str: iso3c of country
	mask_path: type str: path to where the masks are stored
	'''

	print in_file

	# open file to get information
	nc_in=Dataset(in_file,"r")
	lon_in=nc_in.variables['lon'][:]
	lat_in=nc_in.variables['lat'][:]

	# find correct mask
	mask_file=mask_path+str(len(lon_in))+"x"+str(len(lat_in))+"/sov_None_africa.nc"	;	print mask_file
	nc_mask=Dataset(mask_file,"r")
	mask=nc_mask.variables[iso][:,:]

	lon_mask=nc_mask.variables['lon'][:]
	lat_mask=nc_mask.variables['lat'][:]

	# find relevant area (as rectangle)
	lon_mean=np.mean(mask,0)
	lons=np.where(lon_mean!=0)[0]

	lat_mean=np.mean(mask,1)
	lats=np.where(lat_mean!=0)[0]

	nx,ny=len(lons),len(lats)

	# copy netcdf and write zoomed file
	os.system("rm "+out_file)
	nc_out=Dataset(out_file,"w")
	for dname, the_dim in nc_in.dimensions.iteritems():
		if dname=='lon':nc_out.createDimension(dname, nx)
		elif dname=='lat':nc_out.createDimension(dname, ny)
		else:nc_out.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)

	# Copy variables
	for v_name, varin in nc_in.variables.iteritems():
		print v_name
		outVar = nc_out.createVariable(v_name, varin.datatype, varin.dimensions)
					    
		# Copy variable attributes
		outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
					    
		if v_name=='lon':	outVar[:] = lon_mask[list(lons)]
		elif v_name=='lat':	outVar[:] = lat_mask[list(lats)]
		elif v_name==var:	

			# check whether lon and lat are similarly defined in mask and in_file
			if (lat_in in lat_mask) == False:	lats= -np.array(lats)+len(lat_in)
			if (lon_in in lon_mask) == False:	lons= -np.array(lons)+len(lon_in)
			lats,lons=sorted(lats),sorted(lons)

			var_in=nc_in.variables[var][:,list(lats),list(lons)]
			try:	# handle masked array
				masked=np.ma.getmask(var_in)
				var_in=np.ma.getdata(var_in)
				var_in[masked]=np.nan
			except: pass

			# creat a 1-NA mask
			red_mask = mask[np.ix_(list(lats),list(lons))]
			red_mask[red_mask>0]=1
			red_mask[red_mask==0]=np.nan
			var_in=var_in*red_mask
			outVar[:] = var_in[:,:,:]
		else:	outVar[:] = varin[:]


	# close the output file
	nc_out.close()
	nc_in.close()
	print out_file


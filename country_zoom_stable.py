import numpy as np
from netCDF4 import Dataset
import os,gc

def country_zoom(in_file,out_file,var,iso,maskPath='masks/'):
	print in_file
	# open file to get information
	nc_in=Dataset(in_file,"r")
	lon_in=nc_in.variables['lon'][:]
	lat_in=nc_in.variables['lat'][:]

	# find correct mask
	mask_file=maskPath+str(len(lon_in))+"x"+str(len(lat_in))+"/sov_None_africa.nc"	;	print mask_file
	nc_mask=Dataset(mask_file,"r")
	mask=nc_mask.variables[iso][:,:]

	lon_mask=nc_mask.variables['lon'][:]
	lat_mask=nc_mask.variables['lat'][:]

	# find relevant area (as rectangle)
	lon_mean=np.mean(mask,0)
	lons=np.where(lon_mean!=0)

	lat_mean=np.mean(mask,1)
	lats=np.where(lat_mean!=0)

	nx,ny=len(lons[0]),len(lats[0])

	# copy netcdf and write zoomed file
	print out_file
	os.system("rm "+out_file)
	nc_out=Dataset(out_file,"w")
	for dname, the_dim in nc_in.dimensions.iteritems():
		print dname
		if dname=='lon':nc_out.createDimension(dname, nx)
		elif dname=='lat':nc_out.createDimension(dname, ny)
		else:nc_out.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)

	# Copy variables
	for v_name, varin in nc_in.variables.iteritems():
		print v_name
		outVar = nc_out.createVariable(v_name, varin.datatype, varin.dimensions)
					    
		# Copy variable attributes
		outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
					    
		if v_name=='lon':	outVar[:] = lon_mask[list(lons[0])]
		elif v_name=='lat':	outVar[:] = lat_mask[list(lats[0])]
		elif v_name==var:	
			var_in=nc_in.variables[var][:,:,:]
			try:	# handle masked array
				masked=np.ma.getmask(var_in)
				var_in=np.ma.getdata(var_in)
				var_in[masked]=np.nan
			except: pass

			# check whether lon and lat are similarly defined in mask and in_file
			if (lat_in in lat_mask) == False:	var_in[:,:,:]=var_in[:,::-1,:]
			if (lon_in in lon_mask) == False:	var_in[:,:,:]=var_in[:,:,::-1]

			# creat a 1-NA mask
			out_var = var_in[np.ix_(range(var_in.shape[0]),list(lats[0]),list(lons[0]))]
			red_mask = mask[np.ix_(list(lats[0]),list(lons[0]))]
			red_mask[red_mask>0]=1
			red_mask[red_mask==0]=np.nan
			out_var=out_var*red_mask
			outVar[:] = out_var[:,:,:]
		else:	outVar[:] = varin[:]


	# close the output file
	nc_out.close()
	nc_in.close()

	del var_in,out_var,outVar
	gc.collect()



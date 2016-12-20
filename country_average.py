import os,gc
import numpy as np
import glob
import pandas as pd
from netCDF4 import Dataset,netcdftime,num2date

def country_average(in_file,out_file,var,mask_files,countries=None,time_units=None,time_calendar=None):
	'''
	compute weighted country average for each timestep
	in_file: type str: file to be processed
	out_file: type str: file path where output is written
	var: type str: variable name in netcdf file
	mask_files: type list of str: masks to be used	
	countries: type list of str: countries to be evaluated
	time_units: type str: specification for netcdf time variable unit
	time_calendar: type str: specification for netcdf time variable calendar
	'''
	print 'input:',in_file

	nc_data=Dataset(in_file,mode='r')
	var_in=nc_data.variables[var][:,:,:]
	print var_in.shape

	try:	# handle masked array
		masked=np.ma.getmask(var_in)
		var_in=np.ma.getdata(var_in)
		var_in[masked]=np.nan
	except: pass

	# handle time information
	time=nc_data.variables['time'][:]
	datevar = []
	# if specified units and calendar
	if time_units!=None and time_calendar!=None:
		datevar.append(num2date(time,units = time_units,calendar= time_calendar))
	# if no specification
	if time_units==None and time_calendar==None:
		time_unit=nc_data.variables['time'].units
		try:	
			cal_temps = nc_data.variables['time'].calendar
			datevar.append(num2date(time,units = time_unit,calendar = cal_temps))
		except:
			datevar.append(num2date(time,units = time_unit))
	# create index variable
	years=np.array([int(str(date).split("-")[0])\
		for date in datevar[0][:]])
	months=np.array([int(str(date).split("-")[1])\
		for date in datevar[0][:]])
	time_index=np.array([int(str(date).split("-")[0])*100+int(str(date).split("-")[1])\
		for date in datevar[0][:]])

	# make a list of all countries
	if countries==None:
		countries=[]
		for mask_file in mask_files:
			print mask_file
			nc_mask=Dataset(mask_file,mode='r')
			for country in nc_mask.variables:
				if (country!='lon') and (country!='lat'):
					countries.append(country)

	# create output frame
	country_mean = pd.DataFrame(index=time_index,columns=countries)

	for mask_file in mask_files:
		nc_mask=Dataset(mask_file,mode='r')

		if nc_mask.variables['lon'][0]!=nc_data.variables['lon'][0]:
			var_in=var_in[:,:,::-1]
			if nc_mask.variables['lon'][0]!=nc_data.variables['lon'][-1]:
				print 'problem here'
				adasd

		if nc_mask.variables['lat'][0]!=nc_data.variables['lat'][0]:
			var_in=var_in[:,::-1,:]
			if nc_mask.variables['lat'][0]!=nc_data.variables['lat'][-1]:
				print 'problem here'
				adasd

		for country in nc_mask.variables:
			if country in countries:
				mask=nc_mask.variables[country][:,:]
				country_area=np.where(mask>0)				
				for t in range(len(time_index)):
					var_of_area=var_in[t,:,:][country_area]
					# NA handling: sum(mask*var)/sum(mask) for the area where var is not NA
					not_missing_in_var=np.where(np.isnan(var_of_area)==False)[0]	# np.where()[0] because of array([],)
					if sum(mask[country_area][not_missing_in_var])>0:
						country_mean.loc[time_index[t]][country]=sum(mask[country_area][not_missing_in_var]*var_of_area[not_missing_in_var])/sum(mask[country_area][not_missing_in_var])

	# add time information
	country_mean['month']=months
	country_mean['year']=years

	country_mean.to_csv(out_file,float_format='{:f}'.format,index_label='time')
	print 'output:',out_file

	del var_in,country_mean
	gc.collect()


def country_average_of_zoom(inFile,var,maskFile,country='UGA',period=None):
	print file
	nc_data=Dataset(inFile,mode='r')
	var_in=nc_data.variables[var][:,:,:]

	try:	# handle masked array
		masked=np.ma.getmask(var_in)
		var_in=np.ma.getdata(var_in)
		var_in[masked]=np.nan
	except: pass

	var_in[var_in == -np.inf]=np.nan
	var_in[var_in == np.inf]=np.nan

	# extract years from time variable
	time=nc_data.variables['time'][:]
	time_unit=nc_data.variables['time'].units
	datevar = []

	try:	# check if there is calendar information
		cal_temps = nc_data.variables['time'].calendar
		datevar.append(num2date(time,units = time_unit,calendar = cal_temps))
	except:
		datevar.append(num2date(time,units = time_unit))
	years=np.array([int(str(date).split("-")[0])\
		for date in datevar[0][:]])
	
	# prepare outfile						
	country_mean = pd.DataFrame(index=years,columns=[country])


	# get mask
	nc_mask=Dataset(maskFile,mode='r')
	mask=nc_mask.variables[country][:,:]
	lon_mask=nc_mask.variables['lon'][:]
	lat_mask=nc_mask.variables['lat'][:]

	# find relevant area (as rectangle)
	lon_mean=np.mean(mask,0)
	lons=np.where(lon_mean!=0)
	lat_mean=np.mean(mask,1)
	lats=np.where(lat_mean!=0)
	mask=mask[np.ix_(list(lats[0]),list(lons[0]))]

	country_area=np.where(mask>0)
	for t in years:
		var_of_area=var_in[np.where(years==t)[0][0],:,:][country_area]
		# NA handling: sum(mask*var)/sum(mask) for the area where var is not NA
		not_missing_in_var=np.where(np.isnan(var_of_area)==False)[0]	# np.where()[0] because of array([],)
		country_mean.loc[t][country]=sum(mask[country_area][not_missing_in_var]*var_of_area[not_missing_in_var])/sum(mask[country_area][not_missing_in_var])

	country_mean.to_csv(inFile.replace('.nc4','.csv').replace('.nc','.csv'),float_format='{:f}'.format,index_label='time')


def country_average_adm(inFile,var,maskFile,outFile):

	print inFile
	nc_data=Dataset(inFile,mode='r')
	var_in=nc_data.variables[var][:,:,:]

	try:	# handle masked array
		masked=np.ma.getmask(var_in)
		var_in=np.ma.getdata(var_in)
		var_in[masked]=np.nan
	except: pass

	# extract years from time variable
	time=nc_data.variables['time'][:]
	time_unit=nc_data.variables['time'].units
	
	if time_unit!='year':
		datevar = []
		try:	# check if there is calendar information
			cal_temps = nc_data.variables['time'].calendar
			datevar.append(num2date(time,units = time_unit,calendar = cal_temps))
		except:
			datevar.append(num2date(time,units = time_unit))
		years=np.array([int(str(date).split("-")[0])\
			for date in datevar[0][:]])

	if time_unit=='year':
		years=time

	nc_mask=Dataset(maskFile,mode='r')
	countries=[]
	for country in nc_mask.variables:
		if (country!='lon') & (country!='lat'):
			#countries.append(country.encode('ascii', 'ignore'))
			countries.append(country.encode('utf-8'))

	print countries

	country_mean = pd.DataFrame(index=years,columns=countries)		

	for country in nc_mask.variables:
		if country.encode('utf-8') in countries:
			mask=nc_mask.variables[country][:,:]
			country_area=np.where(mask>0)
			for t in years:
				var_of_area=var_in[np.where(years==t)[0][0],:,:][country_area]
				# NA handling: sum(mask*var)/sum(mask) for the area where var is not NA
				not_missing_in_var=np.where(np.isnan(var_of_area)==False)[0]	# np.where()[0] because of array([],)
				country_mean.loc[t][country.encode('utf-8')]=sum(mask[country_area][not_missing_in_var]*var_of_area[not_missing_in_var])/sum(mask[country_area][not_missing_in_var])

	country_mean.to_csv(outFile,float_format='{:f}'.format,index_label='time')





def relative_to_reference(inFile='Uganda_Proj/data/CRU/year_pre_cru_UGA.nc',outFile='Uganda_Proj/data/CRU/anomaly_pre_cru_UGA.nc',var='pre',reference_period=[1986,2005]):

	nc_in=Dataset(inFile)
	var_in=np.ma.masked_invalid(nc_in.variables[var][:,:,:])

	# extract years from time variable
	time=nc_in.variables['time'][:]
	time_unit=nc_in.variables['time'].units
	datevar = []

	try:	# check if there is calendar information
		cal_temps = nc_in.variables['time'].calendar
		datevar.append(num2date(time,units = time_unit,calendar = cal_temps))
	except:
		datevar.append(num2date(time,units = time_unit))
	years=np.array([int(str(date).split("-")[0])\
		for date in datevar[0][:]])

	var_anom=var_in-np.mean(var_in[np.where((years>=reference_period[0]) & (years<reference_period[1]))[0],:,:],axis=0)
		
	# copy netcdf and write zoomed file
	os.system("rm "+outFile)
	nc_out=Dataset(outFile,"w")
	for dname, the_dim in nc_in.dimensions.iteritems():
		print dname
		nc_out.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)

	# Copy variables
	for v_name, varin in nc_in.variables.iteritems():
		print v_name
		outVar = nc_out.createVariable(v_name, varin.datatype, varin.dimensions)
						    
		# Copy variable attributes
		outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
		if v_name==var:	
			outVar[:]=np.ma.masked_invalid(var_anom[:,:,:])			    
		else:	outVar[:] = varin[:]

	nc_out.close()
	nc_in.close()







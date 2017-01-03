#######################################
# create dict for country and variable
#######################################

import numpy as np
from netCDF4 import Dataset,netcdftime,num2date

def prepare_country_dict(var,files):
	country_dict={'support':{}}

	country_dict['support']['rcp_names']=[]
	country_dict['support']['model_names']=[]
	country_dict['support']['files']=files

	for file in files:
		# interprete files
		print file
		for i in range(-6,-2):
			if file.split('_')[i][0:3]=='rcp':
				rcp=file.split('_')[i]
				model=file.split('_')[i-1]
				break

		if model not in country_dict['support']['model_names']: country_dict['support']['model_names'].append(model)
		if rcp not in country_dict['support']['rcp_names']: 
			country_dict['support']['rcp_names'].append(rcp)
			country_dict[rcp]={'models':{}}
		
		nc_in=Dataset(file)

		if len(country_dict['support'].keys())==3:
			country_dict['support']['lon']=nc_in.variables['lon'][:]
			country_dict['support']['lat']=nc_in.variables['lat'][:]
			# time handling
			time=nc_in.variables['time'][:]
			time_unit=nc_in.variables['time'].units
			datevar = []
			try:
				cal_temps = nc_in.variables['time'].calendar
				datevar.append(num2date(time,units = time_unit,calendar = cal_temps))
			except:
				datevar.append(num2date(time,units = time_unit))
			country_dict['support']['year']=np.array([int(str(date).split("-")[0])\
							for date in datevar[0][:]])				
			country_dict['support']['month']=np.array([int(str(date).split("-")[1])\
							for date in datevar[0][:]])	

		country_dict[rcp]['models'][model]=np.ma.masked_invalid(nc_in.variables[var][:,:,:])

	# ensemble mean
	for rcp in country_dict['support']['rcp_names']:
		country_dict[rcp]['ensemble_mean']=country_dict[rcp]['models'][country_dict[rcp]['models'].keys()[0]].copy()*0
		for model in country_dict['support']['model_names']:
			country_dict[rcp]['ensemble_mean']+=country_dict[rcp]['models'][model]
		country_dict[rcp]['ensemble_mean']/=5

	return country_dict
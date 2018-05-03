
import numpy as np
import dimarray as da
import pcse

os.chdir('/Users/peterpfleiderer/Documents/Projects/tropical_cyclones/data/CAR25/spei')


RH=da.read_nc('item3245_daily_mean_p014_2017-06_2017-10.nc')['item3245_daily_mean']
Tmin=da.read_nc('item3236_daily_minimum_p014_2017-06_2017-10.nc')['item3236_daily_minimum']-273.15
Tmax=da.read_nc('item3236_daily_maximum_p014_2017-06_2017-10.nc')['item3236_daily_maximum']-273.15
T=da.read_nc('item3236_daily_mean_p014_2017-06_2017-10.nc')['item3236_daily_mean']-273.15
SWR=da.read_nc('item1235_daily_mean_p014_2017-06_2017-10.nc')['item1235_daily_mean']*(3600.*24.)
Wind2=da.read_nc('item3236_daily_mean_p014_2017-06_2017-10.nc')['item3236_daily_mean']*0.0

es = 6.11 * np.exp((2.5e6 / 461.) * (1 / 273. - 1 / (273. + T)))
VAP= RH / 100. * es

nc=da.read_nc('item3236_daily_mean_p014_2017-06_2017-10.nc')
time_=nc.time2
dates=[num2date(t,units = nc.axes['time2'].units,calendar = nc.axes['time2'].calendar) for t in time_]
lats = nc['global_latitude1'].values

t,y,x=0,0,0
PET=pcse.util.penman_monteith(datetime(2017, 6, 1, 12, 0), lats[y,x], ELEV=0, TMIN=Tmin.values[t,0,y,x], TMAX=Tmax.values[t,0,y,x], AVRAD=SWR.values[t,0,y,x], VAP=VAP.values[t,0,y,x], WIND2=Wind2.values[t,0,y,x])

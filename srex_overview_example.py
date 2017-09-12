import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import cPickle as pickle
import matplotlib.pylab as plt 
import dimarray as da
from scipy.optimize import curve_fit
from lmfit import  Model
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from scipy import stats

os.chdir('/Users/peterpfleiderer/Documents/Projects/Scripts/allgemeine_scripte')
import plot_map as plot_map; reload(plot_map)
import srex_overview as srex_overview; reload(srex_overview)
os.chdir('/Users/peterpfleiderer/Documents/Projects/fahad/')


pkl_file = open('srex_dict.pkl', 'rb')
srex = pickle.load(pkl_file)	;	pkl_file.close()

masks=da.read_nc('360x720_360x720_pr_SREX_masks.nc4')['mask']


# ---------------------------- distr comparison
def legend_plot(subax):
	subax.axis('off')
	for dataset,color in zip(['HadGHCND','MIROC','NORESM1','ECHAM6','CAM4','CanAM4'],['black','blue','green','cyan','magenta','orange']):
		subax.plot([1,1],[1,1],label=dataset,c=color)
	subax.legend(loc='best',fontsize=12)

def example_plot(subax):
	subax.set_ylim((0,120))
	subax.tick_params(axis='x',which='both',bottom='on',top='on',labelbottom='on') 
	subax.tick_params(axis='y',which='both',left='on',right='on',labelleft='on') 
	subax.set_ylabel('bla')
	subax.set_xlabel('')
	subax.set_title('example')
	subax.locator_params(axis = 'x', nbins = 5)

def distrs(subax,region,arg1=None,arg2=None,arg3=None):

	print region

	subax.boxplot(distr_dict[region])
	subax.set_ylim((0,120))
	subax.tick_params(axis='x',which='both',bottom='on',top='on',labelbottom='off') 
	subax.tick_params(axis='y',which='both',left='on',right='on',labelleft='off') 
	subax.locator_params(axis = 'x', nbins = 5)

	subax.annotate('   '+region, xy=(0, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',ha='left', va='bottom')


srex_overview.srex_overview(distrs,srex_polygons=srex,example_plot=example_plot,output_name='test.png')



data=da.read_nc('final_Cd_timmin_pr_day_ECHAM6_All-Hist.nc4')['pr']



distr_dict={}
for region in masks.region:
	if region!='global':
		print region
		reg_mask=masks[region]
		reg_mask[np.isfinite(reg_mask)]=1
		xx=np.asarray(data*reg_mask).reshape(720*360*80)
		distr_dict[region]=xx[np.logical_not(np.isnan(xx))]






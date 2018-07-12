import seaborn as sns

import matplotlib.pylab as plt
from matplotlib.path import Path
import matplotlib
from matplotlib.collections import PatchCollection

import numpy as np

import cartopy.crs as ccrs
import cartopy

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def srex_overview(small_plot_function, axis_settings,  polygons, reg_info, x_ext=[-180,180], y_ext=[-64,-2], small_plot_size=0.05, output_name=None, legend_plot=None, legend_pos=None, arg1=None, arg2=None, arg3=None, fontsize=8, title=None, projection=None):

	if projection is None:
		projection=ccrs.Robinson(central_longitude=0, globe=None)

	asp=float(x_ext[-1]-x_ext[0])/float(y_ext[-1]-y_ext[0])

	# settings for big plot image
	ratio=0.0
	plt.close('all')
	fig=plt.figure(figsize=(13,13/asp))
	ax_map=fig.add_axes([0,0,1,1],projection=projection)
	ax_map.set_global()
	ax_map.coastlines()
	ax_map.set_extent(x_ext+y_ext, crs=ccrs.PlateCarree())
	ax_map.axis('off')
	# ax_map.outline_patch.set_edgecolor('white')
	ratio=0.0

	patches,colors=[],[]
	for region in reg_info.keys():
		# fill the outer subplot with whatever is defined in small_plot_function
		if 'pos' in reg_info[region].keys():
			x,y=reg_info[region]['pos']
		else:
			x,y=Polygon(polygons[region]['points']).centroid.xy
			x,y=x[0],y[0]
			if 'pos_off' in reg_info[region].keys():
				x+=reg_info[region]['pos_off'][0]
				y+=reg_info[region]['pos_off'][1]

		x=abs(x-x_ext[0])/float(abs(x_ext[1]-x_ext[0]))
		y=abs(y-y_ext[0])/float(abs(y_ext[1]-y_ext[0]))

		if 'scaling_factor' in reg_info[region].keys():
			zz=reg_info[region]['scaling_factor']
			ax = fig.add_axes([x-small_plot_size*zz/2.,y-(small_plot_size*zz*0.75*asp*0.5),small_plot_size*zz,small_plot_size*zz*0.75*asp])#,axisbg='w')
		else:
			ax = fig.add_axes([x-small_plot_size/2.,y-(small_plot_size*0.75*asp*0.5),small_plot_size,small_plot_size*0.75*asp])#,axisbg='w')


		small_plot_function(subax=ax,region=region,arg1=arg1,arg2=arg2,arg3=arg3)
		if 'ylabel' in reg_info[region].keys():
			ax=axis_settings(ax,label='on')
			ax.set_ylabel(reg_info[region]['ylabel'],fontsize=fontsize,fontweight='bold')
			ax.set_xlabel(reg_info[region]['xlabel'],fontsize=fontsize,fontweight='bold')
			ax.set_title(reg_info[region]['title'],fontsize=fontsize)
		else:
			ax=axis_settings(ax,label='off')

		# add polygon
		if region in polygons.keys():
			ax_map.add_geometries([Polygon(polygons[region]['points'])], ccrs.PlateCarree(), color=None,alpha=0.3,facecolor=reg_info[region]['color'],hatch=reg_info[region]['hatch'])

	if legend_pos is not None and legend_plot is not None:
		x,y=legend_pos
		x=abs(x-x_ext[0])/float(abs(x_ext[1]-x_ext[0]))
		y=abs(y-y_ext[0])/float(abs(y_ext[1]-y_ext[0]))
		ax = fig.add_axes([x-small_plot_size/2.,y-(small_plot_size*0.75*asp*0.5),small_plot_size,small_plot_size*0.75*asp])
		legend_plot(subax=ax)

	if title is not None:
		title_ax=fig.add_axes([0.2,0.8,0.6,0.2]);	title_ax.axis('off')
		title_ax.annotate(title, xy=(0.5,0.5), xycoords='axes fraction', fontsize=12,fontweight='bold',xytext=(-5, 5), textcoords='offset points',backgroundcolor='white',horizontalalignment='center')


	if output_name!=None: plt.savefig(output_name,dpi=600)
	if output_name==None: return(fig,ax_map)


#
#
# def srex_overview_NH(small_plot_function,srex_polygons,output_name,example_plot=None,legend_plot=None,annotate_plot=None,arg1=None,arg2=None,arg3=None):
#
# 	plt.clf()
# 	# subplot positions
# 	reg_info={}
# 	poly={}
# 	for region in srex_polygons.keys():
# 		reg_info[region]={}
# 		poly[region]={}
#
# 	c1=20
# 	c2=40
# 	c3=60
# 	c4=80
#
# 	reg_info['ALA']={'pos':[0.03,0.6],'color':c1}
# 	reg_info['WNA']={'pos':[0.09,0.33],'color':c2}
# 	reg_info['CNA']={'pos':[0.2,0.47],'color':c3}
# 	reg_info['ENA']={'pos':[0.32,0.3],'color':c1}
# 	reg_info['CGI']={'pos':[0.3,0.7],'color':c4}
# 	reg_info['CAM']={'pos':[0.2,0.04],'color':c4}
#
# 	reg_info['NEU']={'pos':[0.48,0.73],'color':c1}
# 	reg_info['CEU']={'pos':[0.53,0.47],'color':c2}
# 	reg_info['CAS']={'pos':[0.65,0.45],'color':c1}
# 	reg_info['NAS']={'pos':[0.8,0.6],'color':c3}
# 	reg_info['TIB']={'pos':[0.7,0.18],'color':c4}
# 	reg_info['EAS']={'pos':[0.85,0.25],'color':c1}
#
# 	reg_info['MED']={'pos':[0.45,0.2],'color':c3}
# 	reg_info['WAS']={'pos':[0.58,0.04],'color':c4}
#
#
# 	# settings for big plot image
# 	ratio=0.0
# 	plt.close('all')
# 	plate_carree = ccrs.PlateCarree()
# 	fig=plt.figure(figsize=(10,2.5))
# 	ax_map=fig.add_axes([0,0,1,1],projection=plate_carree)
# 	ax_map.set_global()
# 	ax_map.coastlines()
# 	ax_map.set_xlim(-180,180)
# 	ax_map.set_ylim(0,90)
# 	ax_map.axis('off')
# 	ax_map.outline_patch.set_edgecolor('white')
#
#
# 	# # map in the center of the big plot window (transparant background)
# 	# #ax_map=fig.add_axes([ratio,ratio,1-2*ratio,1-2*ratio])
# 	# ax_map=fig.add_axes([0,0,1,1])
# 	# ax_map.patch.set_facecolor('None')
# 	# ax_map.axis('off')
# 	# m=Basemap(ax=ax_map,llcrnrlon=-180,urcrnrlon=180,llcrnrlat=10,urcrnrlat=80)
# 	# m.drawcoastlines()
#
# 	factor_NH=(60.)/(80.+65.)
#
# 	patches,colors=[],[]
# 	for region in srex_polygons.keys():
# 		if region != 'global' and 'pos' in reg_info[region].keys():
# 			# fill the outer subplot with whatever is defined in small_plot_function
# 			ax = fig.add_axes([reg_info[region]['pos'][0],reg_info[region]['pos'][1],0.1,0.25])#,axisbg='w')
# 			small_plot_function(subax=ax,region=region,arg1=arg1,arg2=arg2,arg3=arg3)
#
# 			# add polygon
# 			patches.append(matplotlib.patches.Polygon(srex_polygons[region]['points']))
# 			colors.append(reg_info[region]['color'])
#
# 	# annotate
# 	if annotate_plot is not None:
# 		ax = fig.add_axes([0.0, 0.0, 0.1, 0.1333333333])#,axisbg='w')
# 		annotate_plot(subax=ax,arg1=arg1,arg2=arg2,arg3=arg3)
#
#
# 	# # explanatory plot
# 	# if example_plot is not None:
# 	# 	ax = fig.add_axes([0.09, 0.2, 0.1, 0.1333333333],axisbg='w')
# 	# 	example_plot(subax=ax)
#
# 	# # legend plot
# 	# if legend_plot is not None:
# 	# 	ax = fig.add_axes([0.08, 0.4, 0.1, 0.1333333333],axisbg='w')
# 	# 	legend_plot(subax=ax)
#
# 	# plot colored polygons
# 	p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
# 	#colors = 100*np.random.rand(len(patches))
# 	p.set_array(np.array(colors))
# 	ax_map.add_collection(p)
#
# 	if output_name!=None: plt.savefig(output_name,dpi=600)
# 	if output_name==None: plt.show()
#
#
#
#
# def srex_overview_global(small_plot_function,srex_polygons,output_name=None,example_plot=None,legend_plot=None,annotate_plot=None,arg1=None,arg2=None,arg3=None):
#
# 	# subplot positions
# 	reg_info={}
# 	poly={}
# 	for region in srex_polygons.keys():
# 		reg_info[region]={}
# 		poly[region]={}
#
# 	c1=20
# 	c2=40
# 	c3=60
# 	c4=80
#
# 	reg_info['ALA']={'pos':[0.1,0.8],'color':c1}
# 	reg_info['WNA']={'pos':[0.12,0.63],'color':c2}
# 	reg_info['CNA']={'pos':[0.22,0.66],'color':c3}
# 	reg_info['ENA']={'pos':[0.32,0.6],'color':c1}
# 	reg_info['CGI']={'pos':[0.3,0.8],'color':c4}
# 	reg_info['SSA']={'pos':[0.35,0.23],'color':c4}
# 	reg_info['CAM']={'pos':[0.22,0.5],'color':c4}
# 	reg_info['AMZ']={'pos':[0.32,0.47],'color':c2}
# 	reg_info['NEB']={'pos':[0.37,0.36],'color':c1}
# 	reg_info['WSA']={'pos':[0.24,0.23],'color':c3}
#
# 	reg_info['NEU']={'pos':[0.48,0.84],'color':c1}
# 	reg_info['CEU']={'pos':[0.53,0.70],'color':c2}
# 	reg_info['CAS']={'pos':[0.65,0.72],'color':c1}
# 	reg_info['NAS']={'pos':[0.8,0.8],'color':c3}
# 	reg_info['TIB']={'pos':[0.7,0.62],'color':c4}
# 	reg_info['EAS']={'pos':[0.8,0.63],'color':c1}
# 	reg_info['SAS']={'pos':[0.66,0.5],'color':c2}
#
# 	reg_info['MED']={'pos':[0.45,0.66],'color':c3}
# 	reg_info['WAF']={'pos':[0.47,0.44],'color':c2}
# 	reg_info['SAH']={'pos':[0.49,0.55],'color':c1}
# 	reg_info['SAF']={'pos':[0.53,0.25],'color':c1}
# 	reg_info['EAF']={'pos':[0.56,0.45],'color':c3}
# 	reg_info['WAS']={'pos':[0.58,0.60],'color':c4}
#
# 	reg_info['NAU']={'pos':[0.84,0.3],'color':c2}
# 	reg_info['SEA']={'pos':[0.8,0.48],'color':c3}
# 	reg_info['SAU']={'pos':[0.81,0.18],'color':c1}
#
# 	# settings for big plot image
# 	ratio=0.0
# 	plt.close('all')
# 	plate_carree = ccrs.PlateCarree()
# 	fig=plt.figure(figsize=(12,6))
# 	ax_map=fig.add_axes([0,0,1,1],projection=plate_carree)
# 	ax_map.set_global()
# 	ax_map.coastlines()
# 	ax_map.set_xlim(-180,180)
# 	ax_map.set_ylim(-65,80)
# 	ax_map.axis('off')
# 	ax_map.outline_patch.set_edgecolor('white')
# 	ratio=0.0
#
# 	patches,colors=[],[]
# 	for region in srex_polygons.keys():
# 		if region != 'global':
# 			# fill the outer subplot with whatever is defined in small_plot_function
# 			ax = fig.add_axes([reg_info[region]['pos'][0],reg_info[region]['pos'][1],0.075,0.1])#,axisbg='w')
# 			small_plot_function(subax=ax,region=region,arg1=arg1,arg2=arg2,arg3=arg3)
#
# 			# add polygon
# 			patches.append(matplotlib.patches.Polygon(srex_polygons[region]['points']))
# 			colors.append(reg_info[region]['color'])
#
# 	# plot colored polygons
# 	p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
# 	#colors = 100*np.random.rand(len(patches))
# 	p.set_array(np.array(colors))
# 	ax_map.add_collection(p)
#
# 	if output_name!=None: plt.savefig(output_name,dpi=600)
# 	if output_name==None: return(fig)
#
#
#
# # example plot functions
#
# def global_plot_function(subax):
# 	subax.plot([1,1],[1,1],label='projections')
# 	subax.plot([1,1],[1,1],label='single-exp')
# 	subax.plot([1,1],[1,1],label='double-exp')
# 	subax.set_yscale('log')
# 	subax.set_xlim((0,40))
# 	subax.set_ylim((100,1000000))
# 	subax.tick_params(axis='x',which='both',bottom='on',top='on',labelbottom='on')
# 	subax.tick_params(axis='y',which='both',left='on',right='on',labelleft='on')
# 	subax.set_title('example')
# 	subax.legend(loc='best',fontsize=8)
#
# def test_plot(subax,region):
# 	tmp=region_dict[region]['DJF']['cold']
# 	count=tmp['count']
# 	pers=tmp['period_length']
# 	subax.plot(pers[2::],count[2::])
# 	subax.plot(pers[2::],tmp['single_exp']['best_fit'],label='single '+str(round(tmp['single_exp']['bic'],2)))
# 	subax.plot(pers[2::],tmp['double_exp']['best_fit'],label='double '+str(round(tmp['double_exp']['bic'],2)))
# 	#subax.plot(pers[2::],tmp['two_exp']['best_fit'],label='two '+str(round(tmp['two_exp']['bic'],2)))
# 	subax.set_yscale('log')
# 	subax.set_xlim((0,40))
# 	subax.set_ylim((100,1000000))
# 	subax.tick_params(axis='x',which='both',bottom='on',top='on',labelbottom='off')
# 	subax.tick_params(axis='y',which='both',left='on',right='on',labelleft='off')
# 	if tmp['double_exp']['params']['b2']>tmp['double_exp']['params']['b1']:
# 		subax.plot([2,40],[1000,1000])
# 	subax.annotate('   '+region, xy=(0, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points',ha='left', va='bottom')
#
#
#
# # -------------- original with subplots around small worldmap
#
# # def show_result_old(small_plot_function,global_plot_function,plot_settings,output_name):
# # 	'''
# # 	Creates world map with little subplots around it
# # 	Information about plot arrangement is stored in plot_settings
# # 	The subplots will be filled with the input of small_plot_function
# # 	small_plot_functions can be defined outside of this class. the function name of the defined small_plot_function is given to show_results()
# # 	'''
# # 	plt.clf()
# # 	# settings for big plot image
# # 	ratio=0.2
# # 	fig = plt.figure(figsize=(9.5,6))
#
# # 	# big plot window
# # 	ax_big=fig.add_axes([0,0,1,1])
# # 	ax_big.axis('off')
#
# # 	# map in the center of the big plot window (transparant background)
# # 	ax_map=fig.add_axes([ratio,ratio,1-2*ratio,1-2*ratio])
# # 	ax_map.patch.set_facecolor('None')
# # 	ax_map.axis('off')
# # 	m=Basemap(ax=ax_map)
# # 	m.drawcoastlines()
#
# # 	for region in plot_settings['points'].keys():
# # 		if region != 'global':
# # 			# plot the ploygon on the map
# # 			x,y=Polygon(plot_settings['points'][region]).exterior.xy
# # 			m.plot(x,y,'g')
# # 			# add a point in the center of the region and a line pointing to the outersubplot
# # 			m.plot(np.mean(x),np.mean(y),'og')
# # 			ax_big.plot(plot_settings['line_to_subplot'][region][0:2],plot_settings['line_to_subplot'][region][2:4],'g')
# # 			# add the outer subplot
# # 			ax = fig.add_axes(plot_settings['subplot_window'][region],axisbg='w')
# # 			# fill the outer subplot with whatever is defined in small_plot_function
# # 			small_plot_function(subax=ax,region=region)
#
# # 	# add global subplot
# # 	# ax = fig.add_axes(plot_settings['subplot_window']['global'],axisbg='w')
# # 	ax = fig.add_axes([0.025, 0.019, 0.1, 0.1],axisbg='w')
# # 	global_plot_function(subax=ax)
#
# # 	ax_big.set_xlim([-200,200])
# # 	ax_big.set_ylim([-100,100])
#
# # 	if output_name!=None: plt.savefig(output_name)
# # 	if output_name==None: plt.show()
#
#
#
# # ------ srex polygons
# 	# poly['WSA']=[(-1, -80), (-20, -66), (-50, -72), (-57, -67), (-57, -82), (1, -82)]
# 	# poly['CAS']=[(30, 60), (50, 60), (50, 75), (30, 75)]
# 	# poly['NEB']=[(-20, -34), (-20, -50), (0, -50), (0, -34)]
# 	# poly['NAS']=[(50, 40), (70, 40), (70, 179), (50, 179)]
# 	# poly['CAM']=[(11, -68), (-1, -80), (29, -118), (29, -90)]
# 	# poly['NAU']=[(-30, 110), (-10, 110), (-10, 155), (-30, 155)]
# 	# poly['NEU']=[(48, -10), (75, -10), (75, 40), (61, 40)]
# 	# poly['TIB']=[(30, 75), (50, 75), (50, 100), (30, 100)]
# 	# poly['CGI']=[(50, -12), (50, -105), (85, -105), (85, -12)]
# 	# poly['SAH']=[(15, -20), (30, -20), (30, 40), (15, 40)]
# 	# poly['SAF']=[(-35, -10), (-11, -10), (-11, 52), (-35, 52)]
# 	# poly['EAF']=[(-11, 25), (15, 25), (15, 52), (-11, 52)]
# 	# poly['CEU']=[(45, -10), (48, -10), (61, 40), (45, 40)]
# 	# poly['AMZ']=[(-20, -66), (-1, -80), (11, -69), (11, -50), (-20, -50)]
# 	# poly['SEA']=[(-10, 95), (20, 95), (20, 155), (-10, 155)]
# 	# poly['SAS']=[(5, 60), (30, 60), (30, 100), (20, 100), (20, 95), (5, 95)]
# 	# poly['EAS']=[(20, 100), (50, 100), (50, 145), (20, 145)]
# 	# poly['SAU']=[(-50, 110), (-30, 110), (-30, 179), (-50, 179)]
# 	# poly['ENA']=[(25, -60), (25, -85), (50, -85), (50, -60)]
# 	# poly['WAF']=[(-11, -20), (15, -20), (15, 25), (-11, 25)]
# 	# poly['WNA']=[(29, -105), (29, -130), (60, -130), (60, -105)]
# 	# poly['CNA']=[(50, -85), (29, -85), (29, -105), (50, -105)]
# 	# poly['WAS']=[(15, 40), (50, 40), (50, 60), (15, 60)]
# 	# poly['MED']=[(30, -14), (45, -14), (45, 40), (30, 40)]
# 	# poly['ALA']=[(55, -105), (55, -168), (73, -169), (73, -105)]
# 	# poly['SSA']=[(-20, -39), (-57, -39), (-57, -67), (-50, -72), (-20, -66)]

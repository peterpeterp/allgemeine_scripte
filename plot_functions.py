import numpy as np

from mpl_toolkits.basemap import Basemap, cm
import mpl_toolkits.basemap
import matplotlib.pylab as plt
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as mcolors

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

# converter
col_conv = mcolors.ColorConverter().to_rgb

# simpler method
def plot_map(ax,lon,lat,Z,color_type=plt.cm.bwr,color_range=[0,100],color_label='bla',subtitle='',grey_area=None):
	m = Basemap(ax=ax,llcrnrlon=np.min(lon),urcrnrlon=np.max(lon),llcrnrlat=np.min(lat),urcrnrlat=np.max(lat),resolution="l",projection='cyl')
	m.drawmapboundary(fill_color='1.')

	Z=np.ma.masked_invalid(Z)
	if lat[0]>lat[1]:Z=Z[::-1,:]
	if lon[0]>lon[1]:Z=Z[:,::-1]

	im1 = m.imshow(Z,cmap=color_type,vmin=color_range[0],vmax=color_range[1],interpolation='none')
	if grey_area!=None:
		Z=np.ma.masked_invalid(grey_area.copy())
		if lat[0]>lat[1]:Z=Z[::-1,:]
		if lon[0]>lon[1]:Z=Z[:,::-1]
		im2 = m.imshow(Z,cmap=plt.cm.Greys,vmin=0,vmax=1,interpolation='none')

	m.drawcoastlines()
	m.drawstates()
	m.drawcountries()

	
	if color_label!=None:
		# add colorbar
		cb = m.colorbar(im1,'right', size="5%", pad="2%")

		tick_locator = ticker.MaxNLocator(nbins=5)
		cb.locator = tick_locator
		cb.update_ticks()
		cb.set_label(color_label, rotation=90)

	if subtitle!='':ax.set_title(subtitle)

	return(ax,im1)

# # could be better for specific grid comparisons
# def plot_map(ax,lon,lat,Z,color_type=plt.cm.bwr,color_range=[0,100],color_label='bla',subtitle='',grey_area=None,limits=None):
# 	if limits==None:
# 		limits=[np.min(lon,axis=1)[0]-1,np.max(lon,axis=1)[0]+1,np.min(lat,axis=0)[0]-1,np.max(lat,axis=0)[0]+1]
# 		print limits
		
# 	m = Basemap(ax=ax,llcrnrlon=limits[0],urcrnrlon=limits[1],llcrnrlat=limits[2],urcrnrlat=limits[3],resolution="l",projection='cyl')
# 	m.drawmapboundary(fill_color='1.')

# 	#Z=Z.reshape([lon.shape[0]-1,lon.shape[1]-1])
# 	Zm=np.ma.masked_invalid(Z)

# 	im1 = m.pcolormesh(lon,lat,Zm,cmap=color_type,vmin=color_range[0],vmax=color_range[1])
# 	if grey_area!=None:
# 		grey_area=grey_area.reshape([lon.shape[0]-1,lon.shape[1]-1])
# 		grey_area=np.ma.masked_invalid(grey_area)
# 		im2 = m.pcolormesh(lon,lat,grey_area,cmap=plt.cm.Greys,vmin=0,vmax=1)

# 	m.drawcoastlines()
# 	m.drawstates()
# 	m.drawcountries()

	
# 	if color_label!=None:
# 		# add colorbar
# 		cb = m.colorbar(im1,'right', size="5%", pad="2%")

# 		tick_locator = ticker.MaxNLocator(nbins=5)
# 		cb.locator = tick_locator
# 		cb.update_ticks()
# 		cb.set_label(color_label, rotation=90)

# 	if subtitle!='':ax.set_title(subtitle)

# 	return(ax,im1)

# # start plotting
# def plot_map_old(fig,lon,lat,Z,pos,color_type=plt.cm.bwr,color_range=[0,100],color_label='bla',subtitle='',grey_area=None):
# 	ax = fig.add_subplot(pos)
# 	m = Basemap(llcrnrlon=np.min(lon,axis=1)[0]-1,urcrnrlon=np.max(lon,axis=1)[0]+1,llcrnrlat=np.min(lat,axis=0)[0]-1,urcrnrlat=np.max(lat,axis=0)[0]+1,resolution="l",projection='cyl')
# 	m.drawmapboundary(fill_color='1.')

# 	Z=Z.reshape([lon.shape[0]-1,lon.shape[1]-1])
# 	Zm=np.ma.masked_invalid(Z)

# 	im1 = m.pcolormesh(lon,lat,Zm,cmap=color_type,vmin=color_range[0],vmax=color_range[1])
# 	if grey_area!=None:
# 		grey_area=grey_area.reshape([lon.shape[0]-1,lon.shape[1]-1])
# 		grey_area=np.ma.masked_invalid(grey_area)
# 		im2 = m.pcolormesh(lon,lat,grey_area,cmap=plt.cm.Greys,vmin=0,vmax=1)

# 	m.drawcoastlines()
# 	m.drawstates()
# 	m.drawcountries()
# 	if color_label!=None:
# 		# add colorbar
# 		cb = m.colorbar(im1,"bottom", size="5%", pad="2%")
# 		tick_locator = ticker.MaxNLocator(nbins=5)
# 		cb.locator = tick_locator
# 		cb.update_ticks()
# 		cb.set_label(color_label, rotation=0)

# 	if subtitle!='':ax.set_title(subtitle)

# 	return(fig,ax)










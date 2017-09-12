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
def plot_map(to_plot,lat,lon,color_bar=True,color_label='',color_palette=plt.cm.plasma,color_range=None,grey_area=None,limits=[-180,180,-90,90],ax=None,out_file=None,title='',show=True,figsize=(8,4),coastline_width=0.3,shift_half_a_grid_cell=False,significance=None,marker_size=1,contour=False,levels=None,colors=None):
    if ax==None:
        fig, ax = plt.subplots(nrows=1, ncols=1,figsize=figsize)      

    # handle limits
    if limits is None:
        half_lon_step=abs(np.diff(lon.copy(),1)[0]/2)
        half_lat_step=abs(np.diff(lat.copy(),1)[0]/2)
        relevant_lats=lat[np.where(np.isfinite(to_plot))[0]]
        relevant_lons=lon[np.where(np.isfinite(to_plot))[1]]
        limits=[np.min(relevant_lons)-half_lon_step,np.max(relevant_lons)+half_lon_step,np.min(relevant_lats)-half_lat_step,np.max(relevant_lats)+half_lat_step]


    # handle 0 to 360 lon
    if max(lon)>180:
        problem_start=np.where(lon>180)[0][0]
        new_order=np.array(range(problem_start,len(lon))+range(0,problem_start))
        to_plot=to_plot[:,new_order]
        if significance!=None:
            significance=significance[:,new_order]
        lon=lon[new_order]
        lon[lon>180]-=360

    if limits[0]>180:limits[0]-=360
    if limits[1]>180:limits[1]-=360



    m = Basemap(ax=ax,llcrnrlon=limits[0],urcrnrlon=limits[1],llcrnrlat=limits[2],urcrnrlat=limits[3],resolution="l",projection='cyl')
    m.drawmapboundary(fill_color='1.')

    # show coastlines and borders
    m.drawcoastlines(linewidth=coastline_width)
    m.drawparallels(np.arange(-60,100,30),labels=[0,0,0,0],color='grey',linewidth=0.5) 
    m.drawmeridians([-120,0,120],labels=[0,0,0,0],color='grey',linewidth=0.5)

    # get color_range
    if color_range==None:
        color_range=[np.min(to_plot[np.isfinite(to_plot)]),np.max(to_plot[np.isfinite(to_plot)])]

    # if shift_half_a_grid_cell:
	   #  lon-=np.diff(lon,1)[0]/2.
	   #  lat-=np.diff(lat,1)[0]/2.

    # lon_mesh,lat_mesh=np.meshgrid(lon,lat)


    x,y=lon.copy(),lat.copy()
    x-=np.diff(x,1)[0]/2.
    y-=np.diff(y,1)[0]/2.
    x=np.append(x,[x[-1]+np.diff(x,1)[0]])
    y=np.append(y,[y[-1]+np.diff(y,1)[0]])
    xi,yi=np.meshgrid(x,y)

    to_plot=np.ma.masked_invalid(to_plot)
    if contour:
        x_rel=np.where((lon>=limits[0]) & (lon<=limits[1]))
        y_rel=np.where((lat>=limits[2]) & (lat<=limits[3]))
        xi, yi = np.meshgrid(lon[x_rel], lat[y_rel])
        im = m.contourf(xi,yi,to_plot[np.ix_(y_rel[0],x_rel[0])],levels,extent=limits,colors=colors)
    else:
        im = m.pcolormesh(xi,yi,to_plot,cmap=color_palette,vmin=color_range[0],vmax=color_range[1])


    # significance
    if significance!=None:
        print 'hey'
        xy=np.where(significance!=0)
        print lon[xy[1]],lat[xy[0]]
        ax.scatter(lon[xy[1]],lat[xy[0]],marker='+',color='black',s=marker_size)


    # add colorbar
    if color_bar==True:
        cb = m.colorbar(im,'right', size="5%", pad="2%")
        cb.set_label(color_label, rotation=90)

    ax.set_title(title)
    ax.legend(loc='best')
    
    if out_file==None and show==True:plt.show()
    if out_file!=None:plt.tight_layout() ; plt.savefig(out_file) ; plt.clf()
    return(im)





import os,sys,glob,time,collections,gc,calendar
from netCDF4 import Dataset,netcdftime,num2date
import dimarray as da
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn


def plot_boxplot(ax,distr,x,width,color):
    box=np.nanpercentile(distr,[25,75])
    lim=np.nanpercentile(distr,[0,100])
    ax.fill_between([x-width,x+width],[box[0],box[0]],[box[1],box[1]],color=color,alpha=0.3)
    ax.plot([x,x],[box[0],lim[0]],color=color,linewidth=0.3)
    ax.plot([x,x],[box[1],lim[1]],color=color,linewidth=0.3)
    median=np.nanpercentile(distr,50)
    ax.plot([x-width,x+width],[median,median],color=color)
    ax.plot([x],[np.nanmean(distr)],marker='*',color=color)

# -*- coding: utf-8 -*-
"""
Wildland Fire Assessment System (WFAS)
Created on Wed Dec  2 14:49:58 2020

@author: mjolly
"""
import cartopy.crs as ccrs
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
import geopandas 
#from fiona.crs import from_epsg
from shapely.geometry import  mapping
import cartopy.feature as cfeature
#import rasterio

import rioxarray
import warnings
import os
import cartopy
cartopy.config['data_dir'] = os.getenv('CARTOPY_DIR', cartopy.config.get('data_dir'))

warnings.simplefilter(action='ignore', category=FutureWarning)
# WFASMakeMapImage
# Inputs: url - input GeoTIFF file
#           outFile = Output map image file
#           top = Top Latitude of region of interest
#           left = Left Longitude of region of interest
#           right = Right Longitude of region of interest
#           bottom = Bottom Latitude of region of interest
#           myDate = Data string to include in the map plot
#           product = Shapefile attribute name of variable to plot
#               This sets color maps and colorbar properties
#           myFM = Fuel Model text description
def WFASMakeMapImage(url,outFile="",top = 47 , left = -126, right = -65,
                     bottom =  24,myDate="",product="",myFM="G"):
    #print(product)
    if outFile != "":
        writeFile = True
   
    with xr.open_rasterio(url) as da:
        da.load()
    

    geodf = geopandas.read_file(r"data/cb_2018_us_state_5m.shp")
    #geodf.crs = from_epsg(4326)
    geodf = geodf.to_crs("EPSG:4326")
    
    clipped = da.rio.clip(geodf.geometry.apply(mapping), 
                          geodf.crs,drop=True, invert=False)
    
    
    colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b',
              '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
    class_bins = [0,2,4,6,8,10,15,20, 35]
    # One Hour Fuel Moisture
    if(product == "one_hr_tl_"):
        colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b',
                  '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
        class_bins = [0,2,4,6,8,10,15,20, 65]
        t = "1-hour Fuel Moisture (%s)" % (myDate)
    # Ten Hour Fuel Moisture
    elif(product == "ten_hr_tl_"):
        colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b',
                  '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
        class_bins = [0,2,4,6,8,10,15,20, 35]
        t = "10-hour Fuel Moisture (%s)" % (myDate)
    # Hundred Hour Fuel Moisture
    elif(product == "hun_hr_tl_"):
        colors = ['#d73027','#fc8d59','#fee090','#ffffbf',
                  '#e0f3f8','#91bfdb','#4575b4']
        class_bins = [0,4,6,8,10,15,20,35]
        t = "100-hour Fuel Moisture (%s)" % (myDate)
    # Thousand Hour Fuel Moisture
    elif(product == "thou_hr_tl"):
        colors = ['#d73027','#fc8d59','#fee090','#ffffbf',
                  '#e0f3f8','#91bfdb','#4575b4']
        class_bins = [0,4,6,8,10,15,20,35]
        t = "1000-hour Fuel Moisture (%s)" % (myDate)
    elif(product == "herbaceous"):
        colors = ['#a50026','#d73027','#f46d43',
                  '#fdae61','#fee090','#ffffbf',
                  '#e0f3f8','#abd9e9','#74add1','#4575b4','#313695']
        class_bins = [0,5,10,15,20,30,60,90,120,150,180,250]
        t = "Herbaceous Fuel Moisture (%s)" % (myDate)
    elif(product == "woody_fuel"):
        colors = ['#a50026','#d73027','#f46d43',
                  '#fdae61','#fee090','#ffffbf',
                  '#e0f3f8','#abd9e9','#74add1','#4575b4','#313695']
        class_bins = [0,5,10,15,20,30,60,90,120,150,180,250]
        t = "Woody Fuel Moisture (%s)" % (myDate)
    # Adjective Rating, Fire Danger Class
    elif(product == 'adjective_'):
        colors = ['#1a9641', '#a6d96a', '#ffffbf',  '#fdae61','#d7191c' ]
        class_bins = [0.5,1.5,2.5,3.5,4.5,5.01]
        class_bins = [1,1.8,2.6,3.4,4.2,5]
        #class_bins = [1,2,3,4,5,6]
        t = "Fire Danger Class (%s)" % (myDate)
    elif(product == 'energy_rel'):
        colors = ['#003c30','#01665e','#35978f','#80cdc1',
                  '#c7eae5','#f5f5f5','#f6e8c3','#dfc27d',
                  '#bf812d','#8c510a','#543005']
        #colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b','#e6f598', '#abdda4', '#66c2a5', '#3288bd']
        class_bins = [0,10,20,30,40,50,60,70,80,90,100,130]
        t = "Energy Release Component (Fuel Model %s) (%s)" % (myFM,myDate)
    elif(product == 'kbdi'):
        colors = ['#003c30','#35978f','#80cdc1','#c7eae5',
                  '#f6e8c3','#dfc27d','#bf812d','#543005']
        #colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b','#e6f598', '#abdda4', '#66c2a5', '#3288bd']
        class_bins = [0,100,200,300,400,500,600,700,800]
        t = "Keetch-Byram Drought Index (KBDI) (%s)" % (myDate)
    else:
        colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b',
                  '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
        class_bins = [0,2,4,6,8,10,15,20, 35]
        t = "(%s)" % (myDate)
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(class_bins,len(colors))
    plt.switch_backend('agg')
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.epsg(3857))
   
    im = clipped.plot(ax=ax,cmap=cmap,  norm=norm, add_colorbar=False , transform=ccrs.PlateCarree(), label="Test")
    
    #geodf.plot(ax=ax, transform=ccrs.PlateCarree(),facecolor="none", 
    #          edgecolor='black', lw=0.7)
    geodf.plot(ax=ax, transform=ccrs.PlateCarree(),facecolor="none", 
              edgecolor='black', lw=0.7)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAKES)
    #ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    geodf.plot(ax=ax, transform=ccrs.PlateCarree(),facecolor="none", 
              edgecolor='black', lw=0.7)
    
    #cb = plt.colorbar(im, ticks=class_bins,orientation="horizontal",pad=0.01) #, pad=0.15)
    #cb.set_label("USFS Wildland Fire Assessment System (WFAS)", size='large',weight='bold')
    #cb.ax.tick_params(labelsize='large')
    
    if(product == "adjective_"):
        myTicks = [1.4,2.2,3,3.8,4.6]
        cb = plt.colorbar(im, ticks=myTicks,orientation="horizontal",pad=0.01) #, pad=0.15)
        #cb.set_label(label='Temperature ($^{\circ}$C)', size='large', weight='bold')
        cb.set_label("USFS Wildland Fire Assessment System (WFAS)", size='large',weight='bold')
        cb.ax.tick_params(labelsize='large')
        cb.ax.set_xticklabels(['Low', 'Moderate','High', 'Very High', 'Extreme'])  # horizontal colorbar
    if(product == "hun_hr_tl_"):
        cb = plt.colorbar(im, ticks=[0,4,6,8,10,15,20,35],orientation="horizontal",pad=0.01) #, pad=0.15)
       
        cb.set_label("USFS Wildland Fire Assessment System (WFAS)", size='large',weight='bold')
        cb.ax.tick_params(labelsize='large')
    if(product == "one_hr_tl_" or product == "ten_hr_tl_"):
        cb = plt.colorbar(im, ticks=class_bins,orientation="horizontal",pad=0.01) #, pad=0.15)
        cb.set_label("USFS Wildland Fire Assessment System (WFAS)", size='large',weight='bold')
        cb.ax.tick_params(labelsize='large')
    if(product == "thou_hr_tl"):
        cb = plt.colorbar(im, ticks=class_bins,orientation="horizontal",pad=0.01) #, pad=0.15)
        cb.set_label("USFS Wildland Fire Assessment System (WFAS)", size='large',weight='bold')
        cb.ax.tick_params(labelsize='large')
    if(product == "herbaceous" or product == "woody_fuel"):
        cb = plt.colorbar(im, ticks=class_bins,orientation="horizontal",pad=0.01) #, pad=0.15)
        
        cb.set_label("USFS Wildland Fire Assessment System (WFAS)", size='large',weight='bold')
        cb.ax.tick_params(labelsize='large')
    if(product == 'energy_rel' or product == 'kbdi'): 
        cb = plt.colorbar(im, ticks=class_bins,orientation="horizontal",pad=0.01) #, pad=0.15) 
        cb.set_label("USFS Wildland Fire Assessment System (WFAS)", size='large',weight='bold')
        cb.ax.tick_params(labelsize='large')
        
    ax.set_axis_off()

    ax.set_extent([left,right,bottom,top])
    plt.title(t,fontsize=20,fontweight='bold')
    geodf.plot(ax=ax, transform=ccrs.PlateCarree(),facecolor="none", 
              edgecolor='black', lw=0.7,zorder=3)
    if(writeFile):
        plt.savefig(outFile)
    
#url = r'D:\Temp\outcome11.tif'
#myDate="15-Oct-2020"
#ofile = r'D:\Temp\FM10_%s.jpg' % (myDate)
#WFASMakeMapImage(url,myDate=myDate,outFile=ofile,product="hun_hr_tl_")
#WFASMakeMapImage(url,myDate=myDate,outFile=ofile,top=42.64,left=-96.37,right=-86.26,bottom=36)

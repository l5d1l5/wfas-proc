# -*- coding: utf-8 -*-
"""
@author: mjolly
"""
#from osgeo import gdal
import pandas as pd
from pyWFASHelpers import *
from pyWFASMapMaker import *
from datetime import date #,datetime
import os
import os.path
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Names of downloaded XML file, output shapefile and shapefile layer
xml_fmgf = "wfas_fmg.xml"
layer_fmgf = "wfas_fmg"
shp_fmgf = "%s.shp" % (layer_fmgf)


# Calculate the days past for a historical date
f_date = date(2020, 9, 8)
l_date = date.today() #date(2014, 7, 11)
delta = l_date - f_date
nDays = delta.days
# nDays returns yesterday's values, otherwise it'll return values 
# or the current day
nDays = 1

###############################################################################
# Metadata in the returned shapefile
# Note: Shapefile attributes get truncated to short length than the field names
# in the GeoPandas DataFrame
###############################################################################
meta = ['station_id','station_na','nfdr_date','nfdr_time','latitude','longitude']
# Data variables in the returned shapefile
vars = ['one_hr_tl_', 'ten_hr_tl_', 'hun_hr_tl_','thou_hr_tl', 
        'herbaceous','woody_fuel', 'staffing_c','adjective_','energy_rel','kbdi']
ovars = ['OneHr', 'TenHr', 'HunHr','ThouHrl', 
         'HerbFM','WoodyFM', 'SL','AdjRating','ERC','KBDI']
#tvars = ['adjective_']
#tovars = ['AdjRating']
vnum = 9
product = vars[vnum]

#vars = tvars
#ovars = tvars
#product = 'adjective_'

###############################################################################
# Download WXML, convert to GeoPandas and export it 
# as a shapefile. This only needs to be done once.
###############################################################################
df = MakeWFASShapefile(xml_fmgf, shp_fmgf,nDays=nDays,inFM="",inPriority=1,inOType="N")
df2 = MakeWFASShapefile(xml_fmgf, shp_fmgf,nDays=nDays,inFM="",inPriority=1,inOType="O")
gdf = pd.concat([df,df2])
nind = len(df)
new_index = list(range(0,nind,1))
df.index = new_index
gdf.to_file(shp_fmgf)

myDate=pd.to_datetime(df.nfdr_date[0], format='%m/%d/%Y', 
                      errors='ignore').strftime('%d-%b-%Y')

##############################################################################
# Create the output data directory if it doesn't exist
##############################################################################
my_folder = '/data/wfas'
my_folder = "%s/%s" % (my_folder,myDate)
if not os.path.exists(my_folder):
    os.makedirs(my_folder)

plen = len(vars)

for v in range(0,plen):
    product = vars[v]
    print(product)
    ###############################################################################
    # Interpolate the shapefile to a GeoTIFF
    ###############################################################################
    oTIF = '%s/%s_%s.tif' % (my_folder,product,myDate) #r'D:\Temp\outcome11.tif'
    print(oTIF)
    #oTIF = r'D:\Temp\outcome11.tif'
    MakeWFASGeoTIFF(oTIF,shp_fmgf,layer_fmgf,product)
    
    ###############################################################################
    # Make the map image from the interpolate shapefile 
    ###############################################################################
    oFile = '%s/%s_%s.jpg' % (my_folder,ovars[v],myDate)
    WFASMakeMapImage(oTIF,myDate=myDate,outFile=oFile,product=product)
    #  Missouri and Illinois Regional Example
    #WFASMakeMapImage(url,myDate=myDate,outFile=ofile,top=42.64,left=-96.37,
    #       right=-86.26,bottom=36,product=product)


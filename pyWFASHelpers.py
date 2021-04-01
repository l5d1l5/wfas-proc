# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 09:33:55 2020

@author: mjolly
"""
import xml.etree.ElementTree as et
import pandas as pd
import urllib.request
import geopandas 
from fiona.crs import from_epsg
from osgeo import gdal
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
def parse_XML(xml_file, df_cols): 
    """Parse the input XML file and store the result in a pandas DataFrame with the given columns. 
    The first element of df_cols is supposed to be the identifier variable, which is an attribute of each node element in the 
    XML data; other features will be parsed from the text content of each sub-element. 
    """
    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []
    
    for node in xroot: 
        res = []
        res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[1:]: 
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    out_df = pd.DataFrame(rows, columns=df_cols)
        
    return out_df

def MakeWFASShapefile(xmlfn,shpfn,inFM="7G",nDays="",inPriority="",inOType="O"):
    xml_fmgf = xmlfn
    shp_fmgf = shpfn
    url = 'https://fam.nwcg.gov/wims/xsql/wfas_observation.xsql?stn=&sig=&user=&type=%s&start=&end=&priority=%s&fmodel=%s&time=RS&sort=&ndays=%s' % (inOType,inPriority,inFM,nDays)
    print(url)
    urllib.request.urlretrieve(url, xml_fmgf)

    df = parse_XML(xml_fmgf, ["station_id", "station_name", "nfdr_date", "nfdr_time","nfdr_type", "latitude","longitude",
                              "one_hr_tl_fuel_moisture","ten_hr_tl_fuel_moisture","hun_hr_tl_fuel_moisture",
                              "thou_hr_tl_fuel_moisture","herbaceous_fuel_moisture","woody_fuel_moisture",
                              "staffing_class","adjective_rating","energy_release_component","kbdi"])

    df= df[df.adjective_rating.notnull()]
    df['adjective_rating'] = df['adjective_rating'].str.strip()
    df.rename(columns=lambda x: x.strip(), inplace=True)
    
    df.latitude = df.latitude.astype("float32")
    df.longitude = df.longitude.astype("float32")
    df.hun_hr_tl_fuel_moisture = df.hun_hr_tl_fuel_moisture.astype("float32")
    df.thou_hr_tl_fuel_moisture = df.thou_hr_tl_fuel_moisture.astype("float32")
    df.kbdi = df.kbdi.astype("int32")
    df.dropna()
    mymapping = {'L': 1, 'M': 2, 'H': 3, 'V': 4, 'E': 5}
    df.replace({'adjective_rating': mymapping})
    df[['adjective_rating']] = df[['adjective_rating']].replace(['L','M','H','V','E'], [1, 2, 3,4,5])
    df = df[df.nfdr_type != "F"]
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
    gdf = gdf.set_crs("EPSG:4326")
    gdf.to_file(shp_fmgf)
    return (gdf)

def MakeWFASGeoTIFF(oTIF,iSHP,iLayer,iProduct):
    #print(oTIF,iSHP,iLayer,iProduct)
    CONUSGeogBound= [-135, 55, -60, 20]
    #output = gdal.Grid(r'D:\Temp\outcome10.tif',shp_fmgf,layers='wfas_fmg',zfield='hun_hr_tl_',
    #oTIF = r'D:\Temp\outcome11.tif'
    output = gdal.Grid(oTIF,iSHP,layers=iLayer,zfield=iProduct,#zfield='ten_hr_tl_',
        #algorithm = "invdist:power=2:smoothing=0.0",
        algorithm = "invdist:power=2",
        #algorithm = "nearest:",
        outputBounds=CONUSGeogBound, width=2415,height=1377) 
    #print(output)
    output = None
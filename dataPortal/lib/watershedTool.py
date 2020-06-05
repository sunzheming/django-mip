# This function will return the watershed huc12 number.
# The patameter of the function is x and y of a point.

import json
from arcgis.geometry import intersect, Point, Geometry
import arcgis
from arcgis.gis import GIS
import os
from pyproj import Transformer

gis = GIS()
# the dataset point 

def get_watershed_id(location_data):
#     print(location_data)
    location_data = _location_converter(location_data)
    print(location_data)
    x = float(location_data[1])
    y = float(location_data[0])
    
    # generate the geometry point
    point = [Point({'x': x, 'y': y, 'spatialReference': {"wkid" : 4269}})]
    print(point)
    huc_no = 4
    huc12 = _huc_calculate(point)
    return huc12
# This recursion function used to calculate all the huc no. from the huc4 
def _huc_calculate(point, huc_no=4, huc_last='somethingrandom'):
    # if the huc_no > 12 mean all the huc has been calculated
    if huc_no > 12:
        return huc_last
    path = os.path.dirname(__file__)
    file_name = path + '/huc_data/huc' + str(huc_no) + '.json'
    with open(file_name, 'r') as f:
        data = json.load(f)
    for i in data['data']:
        huc_curr = 'HUC' + str(huc_no)
        huc = i['attributes'][huc_curr]
        # huc_no == 4 mean the first loop
        if huc_no == 4 or huc.startswith(huc_last):
            geo = Geometry({'rings': i['geometry']['rings'], 'spatialReference': {"wkid":4269}})
            result = intersect({"wkid" : 4269}, point, geo)
            # check the return value is none or not, the non value mean the point not in this polygon.
            if result[0]['x'] == 'NaN':
                continue
            else:
                print(huc_no, huc)
                print('==========')
                return _huc_calculate(point, huc_no + 2, huc)

                
# convert wgs84 coordination to web mercator
# receive and return data should be a list like [lat, long]
def _location_converter(location_data):   
    
    # 4326 = wgs84,  3857 = web mercator
    transformer = Transformer.from_crs('epsg:3857', 'epsg:4269')
    web_coor = transformer.transform(location_data[0], location_data[1])
    
    return web_coor              

# get_watershed_id([-122.146692, 37.433208])
 
# This function will accept a json file with the dataset information and
# find the point location in fishnet5, 
# and update the the point data to all others fishnet.

import numpy as np
from arcgis.gis import GIS
import json
from pyproj import Transformer
from configparser import ConfigParser
from datetime import datetime
import ast
import os


class Cell(object):
    def __init__(self, fishnet_data, OID):
        self.top = None
        self.bottom = None
        self.left = None 
        self.right = None
        self.OID = OID
        self.fishnet_data = fishnet_data
    
    def launch_data(self):
        self.top = self.fishnet_data[str(self.OID)]['top']
        self.bottom = self.fishnet_data[str(self.OID)]['bottom']
        self.left = self.fishnet_data[str(self.OID)]['left']
        self.right = self.fishnet_data[str(self.OID)]['right']
        
        
# this function will recieve a uploaded file and update the database and fishnet
# this function will return a file name to flask and save the json file with this name
def income_data(file_data):

    location_OID = _fishnet_update(file_data)    

    return 'success'
        
        

        
        
        
        
def _fishnet_update(new_data):

    wgs_lat = new_data['lat']
    wgs_long = new_data['long']
    
    web_coor = _location_converter([wgs_lat, wgs_long])
    
    web_lat = web_coor[0]
    web_long = web_coor[1]

    # The fishnet 5 matrix information are store in a json file.
    # If the fishnet 5 location update, this json need to update.
#     path=os.path.abspath('.')
    path = os.path.dirname(__file__)    
    with open('%s/fishnet_5.json' % (path)) as json_file:
        fishnet5_data = json.load(json_file)

    # create a empty matrix to find the updated location
    fishnet_matrix = np.empty((160, 160), dtype=np.object)
    OID = 1
    for i in range(160):
        for j in range(160):
            cell = Cell(fishnet5_data, OID)
            cell.launch_data()
            fishnet_matrix[i, j] = cell
            j += 1
            OID += 1
        i += 1
        
    # upsidedown the matrix
    # because the fishnet on the map is start from the left bottom
    fishnet_matrix = np.flipud(fishnet_matrix)
    
    # find the updated data location in the matrix.
    location_x = 0
    location_y = 0
    for i in range(160):
        if fishnet_matrix[i, 0].top < web_long<= fishnet_matrix[i, 0].bottom:
            location_x = i
            break
    for j in range(160):
        if fishnet_matrix[location_x, j].left < web_lat <= fishnet_matrix[location_x, j].right:
            location_y = j
            break
            
    location_OID = fishnet_matrix[location_x, location_y].OID
    
    # Update the data in the fishnet 5
    update_feature_layer(5, location_OID)
    
    # merge the data into others fishnet and update
    _merge_fishnet(4, location_x, location_y)
    
    return location_OID

# convert wgs84 coordination to web mercator
# receive and return data should be a list like [lat, long]
def _location_converter(location_data):   
    
    # 4326 = wgs84,  3857 = web mercator
    transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')
    web_coor = transformer.transform(location_data[0], location_data[1])

    return web_coor

# this function get the fishnet no and OID to update the fishnet data. 
def update_feature_layer(fishnet_no, OID):
    fishnet_order = 5 - fishnet_no
    gis = GIS()
    search_result = gis.content.search('title:jimmy_mip_1')
    map_layer = search_result[0]
    fishnet = map_layer.layers[fishnet_order]
    feature_updated = fishnet.query('OID = %s' % (OID)).features[0]
    feature_updated.attributes['data_count'] += 1
    fishnet.edit_features(updates=[feature_updated])
    
    
# This function will receive a start fishnet_no and location_x and y
# update the all other fishnet data
def _merge_fishnet(fishnet_no, location_x, location_y):
    if fishnet_no == 0:
        return
    new_location_x = _calculate_next_location(location_x)
    new_location_y = _calculate_next_location(location_y)
    fishnet_len = 10 * pow(2, fishnet_no - 1)
    print(fishnet_len)
    new_oid = ((fishnet_len - new_location_x - 1) * fishnet_len) + new_location_y + 1
    print(fishnet_no, new_location_x, new_location_y, new_oid)
#     new_oid = (location_y - 1) * (10 * pow(2, fishnet_no - 1)) + location_x
    update_feature_layer(fishnet_no, new_oid)

    fishnet_no -= 1
    
    return _merge_fishnet(fishnet_no, new_location_x,  new_location_y)

# Calculate the new fishnet x and y location
def _calculate_next_location(old_location):
    if old_location % 2 != 0:
        return round((old_location - 1) / 2)
    else:
        return round(old_location / 2)
    



# income_data('data_12.json')
# _map_count_update(2, 10733)
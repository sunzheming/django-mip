# This function will accept a json file with the dataset information and
# find the point location in fishnet5, 
# and update the the point data to all others fishnet.

import numpy as np
from arcgis.gis import GIS
import json
from datetime import datetime
import ast
import os
result_fishnet = []
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
        
        
# this function will recieve a uploaded file and update the database and fishnet, return a file name to flask and save the json file with this name, example:
# {'fishnet_data': [25441, 6321, 1561, 381, 91]}
def fishnet_tool(location_data):
#     fishnet_data = _fishnet_update(file_data)
    _fishnet_update(location_data)
    analysis_result = {'fishnet_data': result_fishnet}
    return(analysis_result)
        
# input: ['lat', 'long']
# output: OID
def _fishnet_update(location_data):

    web_lat = float(location_data[0])
    web_long = float(location_data[1])


    # The fishnet 5 matrix information are store in a json file.
    # If the fishnet 5 location update, this json need to update.
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
    _update_feature_layer(5, location_OID)
    
    # merge the data into others fishnet and update
    _merge_fishnet(4, location_x, location_y)
    
    return location_OID


# this function get the fishnet no and OID to update the fishnet data. 
def _update_feature_layer(fishnet_no, OID):
    result_fishnet.append(OID)
    fishnet_order = 5 - fishnet_no
    gis = GIS()
    map_layer = gis.content.get('3c6017c113cd4d94a1b414def96ad7e2')
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
    new_oid = ((fishnet_len - new_location_x - 1) * fishnet_len) + new_location_y + 1
    _update_feature_layer(fishnet_no, new_oid)

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

# fishnet_tool(['-13775157.055484595', '4893971.73348189'])
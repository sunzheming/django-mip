from arcgis.gis import GIS
# import pymysql 
import os
import json
from pyproj import Transformer

# this function is used to generate a fishnet 5 geo informaiton json file
# get the data from the arcgis online and generate a json file
# with fishnet location information. 
def generate_fishnet_json():
    gis = GIS()
    # get the feature layers with id
    web_map = gis.content.get('3c6017c113cd4d94a1b414def96ad7e2')
    fishnet_layers = web_map.layers
    fishnet_no = 5
    for layer in fishnet_layers:
        x = 0
        fishnet_json = {}
        fishnet_data = layer.query()
        for i in fishnet_data:
          x += 1
          print(x)
          ring = i.geometry['rings'][0]
#           ring = _location_converter(ring)
          left = ring[0][0]
          right = ring[2][0]
          top = ring[0][1]
          bottom = ring[1][1]
          OID = i.attributes['OID']
          fishnet_json[OID] = {
                  'ring': ring,
                  'left': left,
                  'right': right,
                  'top': top,
                  'bottom': bottom
              }
          
        with open('fishnet_' + str(fishnet_no) + '.json', 'w') as f:
            json.dump(fishnet_json, f)
        fishnet_no -= 1
        print(fishnet_no)

# convert wgs84 coordination to web mercator
# receive and return data should be a list like [lat, long]
def _location_converter(ring):
    result = []
    for location_data in ring:
        # 4326 = wgs84,  3857 = web mercator
        transformer = Transformer.from_crs('epsg:3857', 'epsg:4326')
        wgs_coor = transformer.transform(location_data[0], location_data[1])
        result.append([wgs_coor[1], wgs_coor[0]])
    return result

generate_fishnet_json()
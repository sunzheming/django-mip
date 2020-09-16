from arcgis.gis import GIS
import json 
from arcgis.features import FeatureLayerCollection

def watershed_data_init():
    gis = GIS()
    feature_layers = gis.content.get('2c867326d8e14b489f238cde8fa61a1f')
    map_layers = feature_layers.layers
    huc_no = 8
    x = 0
    for layer in map_layers:
        if huc_no == 2:
            print('Done Done')
            return
        print(layer)
        if x <= 1:
            x += 1
            continue

        print('huc_no:' + str(huc_no) + ', Querting.....')
        features = layer.query()

        print('huc_no:' + str(huc_no) + 'Query Done.')
        huc_rings = {'data': []}
        count = 0
        for feature in features:
            print(count)
            data = feature.as_dict
            huc_rings['data'].append(data)
            count += 1

        file_name = 'huc_data_new/huc' + str(huc_no) + '.json'
        print('huc_no:' + str(huc_no) + ' writeing to json')
        with open(file_name, 'w') as f:
            json.dump(huc_rings, f)
            print(huc_no)
        huc_no  = huc_no - 2
        print('huc_no:' + str(huc_no) + 'Done')

def watershed_validation_init():
    gis = GIS()
    feature_layers = gis.content.get('2c867326d8e14b489f238cde8fa61a1f')
    map_layers = feature_layers.layers

    for layer in map_layers:
#         features = layer.query()
        print(layer)
#         for feature in features:
#             data = feature.as_dict
#             print(data)
#             break
#     file_name = "study_area.json"
#     with open (file_name, 'w') as f:
#         json.dump(data, f)
        
# watershed_validation_init
watershed_data_init()
    
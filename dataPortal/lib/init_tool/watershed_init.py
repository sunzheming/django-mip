from arcgis.gis import GIS
import json 
from arcgis.features import FeatureLayerCollection

def watershed_data_init():
    gis = GIS()
    feature_layers = gis.content.get('fff00941edcc4fa9b3af239dd9ea82c4')
    map_layers = feature_layers.layers
    huc_no = 10
    x = 0
    for layer in map_layers:
        if x == 0:
            x += 1
            continue

        print('huc_no:' + str(huc_no))
        features = layer.query(where='OBJECTID > 0')

        print('huc_no:' + str(huc_no) + 'Query Done.')
        huc_rings = {'data': []}
        count = 0
        for feature in features:
            print(count)
            data = feature.as_dict
            huc_rings['data'].append(data)
            count += 1

        file_name = 'huc_data/huc' + str(huc_no) + '.json'
        print('huc_no:' + str(huc_no) + 'write to json')
        with open(file_name, 'w') as f:
            json.dump(huc_rings, f)
            print(huc_no)
        huc_no  = huc_no - 2
        print('huc_no:' + str(huc_no) + 'Done')

def watershed_validation_init():
    gis = GIS()
    feature_layers = gis.content.get('5f8276a6c14744e5b77660785b29b22c')
    map_layers = feature_layers.layers

    for layer in map_layers:
        features = layer.query()
        for feature in features:
            data = feature.as_dict
    file_name = "study_area.json"
    with open (file_name, 'w') as f:
        json.dump(data, f)
        
watershed_validation_init()
    
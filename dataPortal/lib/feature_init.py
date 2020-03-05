from arcgis.gis import GIS
import pymysql 
from configparser import ConfigParser
import os
# this function is used to generate a fishnet 5 geo informaiton json file
# get the data from the arcgis online and generate a json file
# with fishnet location information. 
def generate_fishnet_json():
    gis = GIS()
    search_result = gis.content.search('title: jimmy_mip_1')
    web_map = search_result[0]
    fishnet_5 = web_map.layers[0]
    fishnet_data = fishnet_5.query()
    

#     fishnet_5_json = {'data': []}
    fishnet_5_json = {}

    for i in fishnet_data:
        ring = i.geometry['rings'][0]
        left = ring[0][0]
        right = ring[2][0]
        top = ring[0][1]
        bottom = ring[1][1]
        OID = i.attributes['OID']
        fishnet_5_json[OID] = {
                'left': left,
                'right': right,
                'top': top,
                'bottom': bottom
            }
    with open('fishnet_5.json', 'w') as f:
        json.dump(fishnet_5_json, f)
    

    
def clean_up_the_fishnet():
    feature_updated = []
    gis = GIS()
    search_result = gis.content.search('title:jimmy_mip_1')
    map_layer = search_result[0]
    fishnet = map_layer.layers
    for i in fishnet:
        layer_data = i.query().features
        for j in layer_data:
            j.attributes['data_count'] = 0
            feature_updated.append(j)
            if (j.attributes['OID'] + 1) % 1000 == 0:
                i.edit_features(updates=feature_updated)
                print(j.attributes['OID'])
                feature_updated = []
        i.edit_features(updates=feature_updated)
        feature_updated = []
    print('Done')

def clean_up_count():
    with DB() as cursor:
#         for i in range(1, 25601):
    
        sql = """UPDATE map_count SET map_list='[]'"""
        cursor.execute(sql)
    
    print('Done')

class DB():
    def __init__(self):
        
        config = ConfigParser()
        path=os.path.abspath('.')
        print(path)
        config.read('%s/config.ini' % (path))
        host = config.get('db_server', 'host')
        user = config.get('db_server', 'user')
        db = config.get('db_server', 'db')
        password = config.get('db_server', 'password')
        
        self.conn = pymysql.connect(host=host, db=db, user=user, passwd=password) 
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
        
    def __enter__(self):
        # return cursor
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):        
        self.conn.commit()
        self.cur.close()     
        self.conn.close()
        
        
clean_up_the_fishnet()
# clean_up_count()
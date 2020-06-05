from arcgis.gis import GIS




def read_metadata():
  
    gis = GIS()
    map_layer = gis.content.get('29364359c0134b41b8b93d5b6f53d25c')
    a = map_layer.properties.extent
    print(a)
  
  
read_metadata()
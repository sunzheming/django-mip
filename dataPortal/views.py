from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

import json
import os
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from .forms import MetadataCollect
from .models import MapData
from django.contrib.auth.models import User, Group
from .lib.fishnet_update import fishnet_tool
from .lib.watershedTool import get_watershed_id

from datetime import datetime
import threading

from pyproj import Transformer

from .models import MapData

from arcgis.geometry import intersect, Point, Geometry


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key/mip-project-270718-5ed8d7aeb413.json"

class Home(TemplateView):
    template_name = 'home.html'



@login_required
def select_file_type(request):

    return render(request, 'select_type.html')

@login_required
def map_picker(request):
    location_data = []
    with open('dataPortal/lib/study_area.json', 'r') as f:
        study_area = json.load(f)
        ring = study_area['geometry']['rings']
    if request.method == 'POST':
        location_data = request.session.get('location_data')['data[]']
        x = float(location_data[0])
        y = float(location_data[1])

        point = [Point({'x': x, 'y': y, 'spatialReference': {"wkid" : 3857}})]
        geometry = Geometry({'rings': ring, 'spatialReference': {"wkid" : 3857}})
        
        print(point, geometry)
        result = intersect({'wkid': 3857}, point, geometry)
        print(result)
        if result[0]['x'] == 'NaN':
            messages.info(request, 'The point you select not in the study area, please try again.')
        else:
            return redirect('upload')
      
    #   for display the study area
    return render(request, 'map_picker.html', {'study_area': ring })

# This function handle the POST request from the JS in web map and save the latitude and longtitude in the session. 
def location_handler(request):
    if request.method == 'POST':
        request_body_dict = dict(request.POST)
        # save the geolocation information to the session
        request.session['location_data'] = request_body_dict
        return HttpResponse(200, 'Done')
    
@login_required
def upload(request):

    if request.method == 'POST':
        form = MetadataCollect(request.POST, request.FILES)
        if form.is_valid():
            # init the loading status to 1
            request.session['loading_status'] = 1
            location_data = request.session.get('location_data')['data[]']
            fishnet_data = fishnet_tool(location_data)
            huc12 = get_watershed_id(location_data)

            # test data
#             fishnet_data = {'fishnet_data': [1,2,3,4,5]}
#             huc12 = '123123123123'

            # convert the web mercator to wgs84
            location_data = _location_converter(location_data)

            # handle the metadata. save the huc and fishnet data to database.
            request_body = request.POST
            latitude = location_data[0]
            longitude = location_data[1]


        #           correct the format problem
            begin_date = None if request_body['begin_date'] == '' else request_body['begin_date']
            end_date = None if request_body['end_date'] == '' else request_body['end_date']

            map_data = MapData.objects.create(title=request_body['title'],
                                              abstract = request_body['abstract'],
                                              begin_date = begin_date,
                                              end_date = end_date,

                                              note = request_body['note'],
                                              latitude=latitude,
                                              longitude=longitude,
                                              fishnet_1=fishnet_data['fishnet_data'][4],
                                              fishnet_2=fishnet_data['fishnet_data'][3],
                                              fishnet_3=fishnet_data['fishnet_data'][2],
                                              fishnet_4=fishnet_data['fishnet_data'][1],
                                              fishnet_5=fishnet_data['fishnet_data'][0], 
                                              huc_4 = huc12[:4],
                                              huc_6 = huc12[:6],
                                              huc_8 = huc12[:8],
                                              huc_10 = huc12[:10],
                                              huc_12 = huc12,
                                              file_location = request.FILES['file_location'],
                                              uploader = request.user
                                              )
            map_data.tags.set(tuple(request_body.getlist('tags')))
            map_data.author.set(request_body.getlist('author'))
            map_data.access_group.set(request_body.getlist('access_group'))
            map_data.save()
            request.session['loading_status'] = 0
#             t = threading.Thread(target=_uploaded_handler, args=[request])
            return render(request, 'success.html', {'data_id':map_data.data_id})
        else:
            print('NOT PASSED')
            print(form.errors)
    else:
        form = MetadataCollect()

    return render(request, 'upload.html', {'form': form})            
            
            
# convert wgs84 coordination to web mercator
# receive and return data should be a list like [lat, long]
def _location_converter(location_data):   
    
    # 4326 = wgs84,  3857 = web mercator
    transformer = Transformer.from_crs('epsg:3857', 'epsg:4326')
    web_coor = transformer.transform(location_data[0], location_data[1])
    
    return web_coor           


@login_required
def map_list(request):
    if request.user.is_superuser:
        maps = MapData.objects.all().order_by('-data_id')
    else:
        user_group = request.user.groups.values_list('id', flat=True)
        group_list = tuple(user_group)
        maps = MapData.objects.filter(access_group__in=group_list).order_by('-data_id')
    maps_p = _data_pagination(maps, request)
#     _handle_ring_data(maps_p)
    mapdata_array = []
    for i in maps_p:
        data = {
            'data_id': i.data_id,
            'fishnet_1': i.fishnet_1,
            'fishnet_2': i.fishnet_2,
            'fishnet_3': i.fishnet_3,
            'fishnet_4': i.fishnet_4,
            'fishnet_5': i.fishnet_5,
        }
        mapdata_array.append(data)
        

    return render(request, 'map_list.html', {
        'maps': maps_p,
        'map_data': mapdata_array
    })
  

@login_required
def search(request):
    keyword = request.GET.get('keyword')
    huckeyword = request.GET.get('huckeyword')
    error_msg = ''
    if not keyword and not huckeyword:
        error_msg = 'Please entry the search word.'
    elif huckeyword:
        map_data = MapData.objects.filter(huc_12__icontains=huckeyword)
    else:
        map_data = MapData.objects.filter(title__icontains=keyword)
    data_list = _data_pagination(map_data, request)
    return render(request, 'map_list.html', {'error_msg': error_msg, 'maps': data_list, 'map_data': map_data})

def _handle_ring_data(data):
    pass

def _data_pagination(data, request):
    paginator = Paginator(data, 10)
    page = request.GET.get('page', 1)
    try:
        maps_p = paginator.page(page)
    except PageNotAnInteger:
        maps_p = paginator.page(1)
    except EmptyPage:
        maps_p = paginator.page(paginator.num_pages)
    return maps_p
  
  
@login_required
def detail(request, pk):
    dataset = get_object_or_404(MapData, pk=pk)
    return render(request, 'detail.html', context={'dataset': dataset})

@login_required
def download(request, filename):
    file_path = 'uploaded/%s' % (filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def success(request):
    
    return render(request, 'success.html')

    

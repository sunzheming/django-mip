from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
import json
import os
from django.contrib import auth

from django.contrib.auth.decorators import login_required

from .forms import UploadFileForm
from .models import MapData
from .lib.fishnet_update import income_data


class Home(TemplateView):
    template_name = 'home.html'
    
    
@login_required
def upload(request):
    context = {}
    
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        
        data_id = _handle_uploaded_file(uploaded_file)
        
        fs = FileSystemStorage()
        name = fs.save(str(data_id), uploaded_file)
        context['url'] = fs.url(name)
        
        return HttpResponseRedirect('/upload/')
    return render(request, 'upload.html', context)



    
def _handle_uploaded_file(file):
    file_data = json.load(file)
    data_url = file_data['data_url']
    title = file_data['title']
    lat = file_data['lat']
    longt = file_data['long']
    save_data = MapData.objects.create(title=title,
                          data_url=data_url,
                          latitude=lat,
                          longtitude=longt,
                          )
    
    data_id = save_data.pk
    
    result = income_data(file_data)
    print(result)
    return data_id

@login_required
def map_list(request):
    maps = MapData.objects.all().order_by('-map_id')
    return render(request, 'map_list.html', {
        'maps': maps
    })

@login_required
def download(request, filename):
    file_path = 'uploaded/%s' % (filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404



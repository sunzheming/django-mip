from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
import json
from django.contrib import auth


from .forms import UploadFileForm
from .models import MapData
from .lib.fishnet_update import income_data


class Home(TemplateView):
    template_name = 'home.html'

def upload(request):
    context = {}
    
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        
        data_id = handle_uploaded_file(uploaded_file)
        
        fs = FileSystemStorage()
        name = fs.save(str(data_id), uploaded_file)
        context['url'] = fs.url(name)
        
        return HttpResponseRedirect('/upload/')
    return render(request, 'upload.html', context)



    
def handle_uploaded_file(file):
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

    
def map_list(request):
    maps = MapData.objects.all()
    return render(request, 'map_list.html', {
        'maps': maps
    })



# def login(request):
#     return render(request, "login.html")


# def login_check(request):
#     username = request.POST.get("username", "")
#     password = request.POST.get("password", "")
#     user = auth.authenticate(request, username=username, password=password)
#     if user is not None:
#         auth.login(request, user)
#         return redirect("/dashboard/")
#     else:
#         return render(request, "login.html", {"message": "登录名或密码错误！"})

    
# def upload_file(request):
#     if request.method == 'POST':
#         print('=======')
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             form = UploadFileForm()
#         return render(request, 'upload.html', {
#             'form': form
#         })
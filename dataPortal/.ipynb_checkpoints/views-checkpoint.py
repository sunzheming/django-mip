from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from datetime import datetime
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage


class Home(TemplateView):
    template_name = 'home.html'

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(str(datetime.now()), uploaded_file)
        context['url'] = fs.url(name)
        print(context)
    return render(request, 'upload.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = UploadFileForm()
        return render(request, 'upload.html', {
            'form': form
        })
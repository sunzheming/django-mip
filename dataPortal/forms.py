from django import forms
from .models import  MapData


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = MapData
        fields = ('extra_data', 
                  'file_location',
                  'title',
                  'data_url',
                 )
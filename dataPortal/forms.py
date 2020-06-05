from django import forms
from .models import  MapData, Tag, Author


# class FileUpload(forms.Form):

    
#     tag_list = ((str(i), Tag.objects.all()[i].name) for i in range(len(Tag.objects.all())))



#     title = forms.CharField(label='Title', max_length=100)
#     tag = forms.MultipleChoiceField(label='Tag', choices = tag_list)
#     abstract = forms.CharField(label='Abstract', max_length=300)
#     keyword = forms.CharField(label='Keyword', max_length=300)
#     begin_date = forms.DateField(label='Begin Date')
#     end_data = forms.DateField(label='End Date')

class MetadataCollect(forms.ModelForm):
    class Meta:
#         test = forms.BooleanField(label='test')
        model = MapData
#         fields = ['title', 'abstract', 'method', 'begin_date', 'end_date', 'author', 'tags', 'south', 'east', 'north', 'west', 'file_location']
        fields = ['title', 'abstract', 'begin_date', 'end_date', 'author', 'tags', 'method', 'note', 'access_group', 'file_location']
        widgets = {
            'title': forms.TextInput(
                attrs = {'class': 'form-control', 'placeholder': 'Title', 'maxlength': '50'}
            ),
            'abstract': forms.Textarea(
                attrs = {'class': 'form-control', 'placeholder': 'Abstract'}
            ),
            'method': forms.Textarea(
                attrs = {'class': 'form-control', 'placeholder': 'method'}
            ),
            'note': forms.Textarea(
                attrs = {'class': 'form-control', 'placeholder': 'Note'}
            ),
            'begin_date': forms.DateInput(
                attrs = {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}
            ),
            'end_date': forms.DateInput(
                attrs = {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}
            ),
            'tags': forms.SelectMultiple(
                attrs = {'class': 'form-control', 'field': 'name'}
            ),
            'author': forms.SelectMultiple(
                attrs = {'class': 'form-control'}
            ),
            'access_group': forms.SelectMultiple(
                attrs = {'class': 'form-control'}
            )
        }
  


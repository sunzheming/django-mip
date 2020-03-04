from django.db import models
from django.contrib.auth.models import User
 
 
class MapData(models.Model):
    map_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    data_url = models.CharField(max_length=255, null=True)
    user_name = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=64, null=True)
    longtitude = models.CharField(max_length=64, null=True)
    date_created = models.DateTimeField(auto_now=True)
    data_modified = models.DateTimeField(auto_now=True)
    extra_data = models.TextField(null=True)
    file_location = models.FileField(upload_to='uploaded/', default=None)
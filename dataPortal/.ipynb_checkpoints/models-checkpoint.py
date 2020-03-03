from django.db import models
from django.contrib.auth.models import User
 
 
class MapData(models.Model):
    map_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    data_url = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    latitude = models.CharField(max_length=64)
    longtitude = models.CharField(max_length=64)
    date_created = models.DateTimeField()
    data_modified = models.DateTimeField()
    extra_data = models.TextField(null=True)
    file_location = models.FileField(upload_to='uploaded/', default=None)
from django.db import models
from django.contrib.auth.models import User, Group
 
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
      return self.name
    
    
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    role = models.CharField(max_length=50, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    
    def __str__(self):
        return self.first_name + self.last_name
      
      
class MapData(models.Model):
    data_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    data_url = models.CharField(max_length=255)
    latitude = models.CharField(max_length=64)
    longitude = models.CharField(max_length=64)
    fishnet_1 = models.IntegerField(null=True)
    fishnet_2 = models.IntegerField(null=True)
    fishnet_3 = models.IntegerField(null=True)
    fishnet_4 = models.IntegerField(null=True)
    fishnet_5 = models.IntegerField(null=True)
    huc_4 = models.CharField(max_length=64, null=True)
    huc_6 = models.CharField(max_length=64, null=True)
    huc_8 = models.CharField(max_length=64, null=True)
    huc_10 = models.CharField(max_length=64, null=True)
    huc_12 = models.CharField(max_length=64, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)
    file_location = models.FileField(upload_to='uploaded/', default=None)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    tags = models.ManyToManyField(Tag)
    method = models.TextField(blank=True)
    abstract = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    begin_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    author = models.ManyToManyField(Author, blank=True)
    access_group = models.ManyToManyField(Group)

class MapHandlerProcessing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    huc_12 = models.CharField(max_length=64, blank=True)
    fishnet_1 = models.IntegerField(blank=True)
    fishnet_2 = models.IntegerField(blank=True)
    fishnet_3 = models.IntegerField(blank=True)
    fishnet_4 = models.IntegerField(blank=True)
    fishnet_5 = models.IntegerField(blank=True)
    status = models.CharField(max_length=32)
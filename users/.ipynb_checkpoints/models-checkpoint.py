from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
 
 
class User(AbstractUser):
#     user_title = models.CharField(max_length=50, null=True)
 
    class Meta(AbstractUser.Meta):
        pass
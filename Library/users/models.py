from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=255)
    email= models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# Create your models here.
class Location(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date_added = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    #sticker_img = models.ImageField(upload_to='images/')
    sticker_img = CloudinaryField('image')

    def __str__(self):
        return self.city

class Countries(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name
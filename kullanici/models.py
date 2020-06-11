from django.db import models
import django.contrib.postgres.fields
from django.contrib.postgres.fields.array import ArrayField


class Kullanici(models.Model):
    userID = models.CharField(max_length=35)
    userName = models.CharField(max_length=20,blank=True, null=True)
    emailOrPhone = models.CharField(max_length=30)
    fotoUrl = models.CharField(max_length=200,default="https://pngimage.net/wp-content/uploads/2018/06/profile-png-icon-1.png")
    followers = ArrayField(
        models.CharField(max_length=30, blank=True, null=True),blank=True, null=True)
    following = ArrayField(
        models.CharField(max_length=30, blank=True,null=True),blank=True, null=True)
    bildirim = ArrayField(models.CharField(max_length=30, blank=True,null=True),blank=True, null=True)
    checkIn = ArrayField(models.CharField(max_length=30, blank=True,null=True),blank=True, null=True)
    checkinTarih = ArrayField(models.CharField(max_length=20, blank=True,null=True),blank=True, null=True)
    mesafe = models.FloatField(default=2)
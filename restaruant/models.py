from django.db import models
import django.contrib.postgres.fields
from django.contrib.postgres.fields.array import ArrayField


# Create your models here.
class Restaruant(models.Model):
    restaruantAd = models.CharField(max_length=20, blank=True, null=True)
    checkin = ArrayField(models.CharField(
        max_length=30, blank=True, null=True), blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    imageUrl = models.ImageField(upload_to='pics', blank=True)
    alkol = models.BooleanField(default=False)
    canliMuzik = models.BooleanField(default=False)
    okey = models.BooleanField(default=False)
    nargile = models.BooleanField(default=False)
    kutuOyunlari = models.BooleanField(default=False)
    acilis = models.TimeField()
    kapanis = models.TimeField()
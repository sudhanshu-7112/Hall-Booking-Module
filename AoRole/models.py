from django.db import models

# Create your models here.

class Conference_Hall(models.Model):
    Hall_name=models.CharField(max_length=30)
    Description=models.CharField(max_length=150)
    occupancy=models.IntegerField()
    max_booking_days=models.IntegerField()
    occupied=models.BooleanField(default=False)

class Conference_Images(models.Model):
    Hall=models.ForeignKey(Conference_Hall, on_delete=models.CASCADE, related_name='hall')
    image=models.FileField(upload_to='images')
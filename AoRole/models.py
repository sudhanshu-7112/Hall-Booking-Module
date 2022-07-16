from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Conference_Hall(models.Model):
    Hall_name = models.CharField(max_length=30)
    Description = models.CharField(max_length=150)
    occupancy = models.IntegerField()
    max_booking_days = models.IntegerField()

class Conference_Images(models.Model):
    Hall = models.ForeignKey(
        Conference_Hall, on_delete=models.CASCADE, related_name='hall')
    image = models.FileField(upload_to='images')


class Pending_Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    Participant_count = models.IntegerField()


class Booked_Hall(models.Model):
    hall = models.ForeignKey(Conference_Hall, on_delete=models.CASCADE)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()


class DynamicPanel(models.Model):
    role = models.CharField(max_length=3)
    name = models.CharField(max_length=15)
    url = models.CharField(max_length=30)


class Departments(models.Model):
    department = models.CharField(max_length=5)


class UserDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)


class Hall_booking_Form(models.Model):
    emp_name = models.CharField(max_length=30)
    emp_department = models.ForeignKey(
        UserDepartment, on_delete=models.CASCADE)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    Participant_count = models.IntegerField()
    Hall_name = models.ForeignKey(Conference_Hall, on_delete=models.CASCADE)
    purpose = models.TextField()
    emp_remark = models.TextField(blank=True, null=True)
    submit_time_emp = models.DateTimeField()
    Hod_remark = models.TextField(blank=True, null=True)
    Hod_approval = models.BooleanField(blank=True, null=True)
    time_stamp_Hod = models.DateTimeField(blank=True, null=True)
    Ao_remark = models.TextField(blank=True, null=True)
    time_stamp_AO = models.DateTimeField(blank=True, null=True)
    booked = models.BooleanField(blank=True, null=True)

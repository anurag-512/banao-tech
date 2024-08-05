from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime, timedelta

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/')

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_full_name()

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(editable=False)

    def save(self, *args, **kwargs):
        # Calculate end time (45 minutes after start time)
        self.end_time = (datetime.combine(self.date, self.start_time) + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with {self.doctor.user.get_full_name()} on {self.date} at {self.start_time}"

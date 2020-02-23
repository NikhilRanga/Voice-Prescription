from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
# Create your models here.

class Users(User):
    PATIENT = 1
    DOCTOR = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (ADMIN, 'Admin'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age=models.IntegerField()

    def __str__(self):
        return self.username

class Patient(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Doctor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    Education = models.CharField(max_length=500)
    License = models.ImageField(upload_to='DoctorLicense')
    AadharNo=models.IntegerField()
    Specialization=models.CharField(max_length=500)


    def __str__(self):
        return self.user.username

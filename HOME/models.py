from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.shortcuts import reverse


class Users(AbstractUser):
    PATIENT=1
    DOCTOR=2
    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age=models.IntegerField(null=True)
    phoneno=models.BigIntegerField()
    address=models.TextField(null=True)

    def __str__(self):
        return self.username

class Patient(models.Model):
    user=models.OneToOneField(Users,on_delete=models.CASCADE,primary_key=True)
    def __str__(self):
        return self.user

class Doctor(models.Model):
    user=models.OneToOneField(Users,on_delete=models.CASCADE,primary_key=True)
    Education=models.CharField(max_length=500)
    Specialization=models.CharField(max_length=500)
    AadharNo=models.IntegerField()
    License=models.FileField(upload_to='License')
    def __str__(self):
        return self.user


class Complaint(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Complaint_Name=models.CharField(max_length=500)
    Symptom1=models.CharField(max_length=500)
    Symptom2=models.CharField(max_length=500)

    def _str_(self):
        return self.Complaint_Name


class Prescription(models.Model):
    PATIENT=Patient.objects.all()
    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
    )
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Date=models.DateTimeField()
    Description=models.TextField()







    
    

     


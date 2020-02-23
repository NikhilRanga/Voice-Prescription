from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Users,Patient,Doctor

# Register your models here.
admin.site.register(Users)
admin.site.register(Patient)
admin.site.register(Doctor)
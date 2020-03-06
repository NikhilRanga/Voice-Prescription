from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Users
from .models import Doctor
from .models import Patient,Complaint


# Register your models here.
admin.site.register(Users)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Complaint)

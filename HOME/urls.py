from django.contrib import admin
from django.urls import path
from . import views
from .views import ComplaintListView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.HomePage,name='HomePage'),
    path('register',views.UserRegister,name='UserRegister'),
    path('patient_signup',views.patient_signup,name='patient_signup'),
    path('doctor_signup',views.doctor_signup,name='doctor_signup'),
    path('Login',auth_views.LoginView.as_view(template_name='Login.html'),name='Login'),
    path('Logout',auth_views.LogoutView.as_view(),name='Logout'),
    path('PatientProfile',views.PatientProfile,name='PatientProfile'),
    path('DoctorProfile',views.DoctorProfile,name='DoctorProfile'),
    path('ComplaintRegistration',views.ComplaintRegistration,name='ComplaintRegistration'),
    path('ComplaintView',views.ComplaintListView,name='ComplaintView'),
    path('ComplaintView/<int:id>/',views.ComplaintDetailView,name='ComplaintDetail'),
    path('pdf',views.GeneratePdf,name='pdf'),
    path('recording/<int:primary_key>/',views.speech_to_text,name='recording'),
    path('PrescriptionForm/<int:primary_key>/',views.PrescriptionForm,name='PrescriptionForm'),
    path('DoctorComplaintView',views.DoctorComplaintView,name='DoctorComplaintView')
   
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
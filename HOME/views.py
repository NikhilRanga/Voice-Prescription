from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Users,Patient,Doctor
from .forms import UserRegisterForm
from .forms import DoctorRegisterForm 
from django import forms
from .utils import render_to_pdf
from django.views.generic import View

# Create your views here.
def HomePage(request):
    return render(request,'home.html',{})


def UserRegister(request):
    return render(request,'UserRegister.html')


def UserBlog(request):
    return render(request,'PatientBlog.html',{})


def patient_signup(request):
    if request.method=='POST':
        userform=UserRegisterForm(request.POST,prefix='userform')
        if userform.is_valid():
            user = userform.save()
            user.role = Users.PATIENT
            user.age = request.POST.get('Age')
            user.save()
            patient = Patient(user=user)
            patient.save()
            username = userform.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('Login')
    else:
        userform = UserRegisterForm(prefix='userform')
        # patientform = PatientSignupForm(request.POST, prefix='patientform')
        return render(request=request, template_name='Patient_Signup.html',context={'form': userform})


def doctor_signup(request):
    if request.method=='POST':
        userform=UserRegisterForm(request.POST,request.FILES,prefix='userform')
        doctorform=DoctorRegisterForm(request.POST,request.FILES,prefix='doctorform')
        if userform.is_valid() and doctorform.is_valid:
                user = userform.save()
                user.role = Users.DOCTOR
                doctor=doctorform.save()
                doctor.user=user
                '''doctor=Doctor(user=user)
                doctor.Education=request.POST.get('Education')
                doctor.License=request.FILES.get('License')
                doctor.Specialization=request.POST.get('Specialization')
                doctor.AadharNo=request.POST.get('AadharNo')'''
                doctor.save()
                username = userform.cleaned_data.get('username')
                messages.success(request,f'Account created for {username}')
                return redirect('Login')
        else:
            print(userform.errors,doctorform.errors)
    else:
        userform = UserRegisterForm(prefix='userform')
        doctorform = DoctorRegisterForm(prefix='doctorform')
        return render(request=request, template_name='Doctor_Signup.html',context={'form': userform,'dform': doctorform})





def GeneratePdf(request):
        data = { 
            
      }
        pdf = render_to_pdf('Prescription.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


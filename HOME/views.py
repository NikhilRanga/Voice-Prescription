from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import DoctorRegisterForm,ComplaintRegisterForm
from .models import Users
from .models import Doctor
from .models import Patient,Complaint,Prescription
from django import forms
from .utils import render_to_pdf
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import speech_recognition as sr
from VoicePrescription.settings import EMAIL_HOST_USER
import datetime
import nexmo

client = nexmo.Client(key='d0b6e5c8', secret='PB26ooSQuHpBUCly')

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
        if userform.is_valid() and doctorform.is_valid() :
                user = userform.save()
                user.role = Users.DOCTOR
                user.save()
                doctor=Doctor(user=user)
                doctor.Education=request.POST.get('Education')
                doctor.License=request.FILES.get('License')
                doctor.Specialization=request.POST.get('Specialization')
                doctor.AadharNo=request.POST.get('AadharNo')
                doctor.save()
                username = userform.cleaned_data.get('username')
                messages.success(request,f'Account created for {username}')
                return redirect('Login')
        else:
            print(userform.errors)
    else:
        userform = UserRegisterForm(prefix='userform')
        doctorform = DoctorRegisterForm(request.POST,request.FILES,prefix='doctorform')
        context={'form': userform,'doctorform':doctorform}
        return render(request,'Doctor_Signup.html',context)




@login_required
def GeneratePdf(request):
    DoctorName=request.user.username
    Date=datetime.date.today
    doctor=Doctor.objects.get(user=request.user)
    prescription=Prescription.objects.get(Doctor=doctor)
    Description=prescription.Description
    Specialization=doctor.Specialization
    data = { 
        'DoctorName':DoctorName,
        'Date':Date,
        'Specialization': Specialization,
        'Description': Description
    }
    pdf = render_to_pdf('Prescription.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required
def ComplaintRegistration(request):
    if request.method =='POST':
            patient=Patient(user=request.user)
            complaint=Complaint(patient=patient)
            complaint.Complaint_Name=request.POST.get("Complaint")
            complaint.Symptom1=request.POST.get('Symptom1')
            complaint.Symptom2=request.POST.get('Symptom2')
            complaint.save()    
            messages.success(request,f'Complaint Registered')
            return redirect('HomePage')
    else:
        return render(request,'ComplaintRegistration.html',{})

class ComplaintListView(ListView):
    model=Complaint
    template_name='ComplaintView.html'
    context_object_name='complaints'

    def get_queryset(self):
       return super(ComplaintListView, self).get_queryset().filter(patient=self.request.user.patient)


class ComplaintDetailView(DetailView):
    model=Complaint
    template_name='ComplaintDetail.html'
    

@login_required
def PrescriptionForm(request):
    return render(request,'PrescriptionForm.html',{})

@login_required
def speech_to_text(request):
    Description=request.POST.get('Description')
    r=sr.Recognizer()
    mic=sr.Microphone()
    with mic as source:
        audio=r.record(source,duration=10)
    try:
        output=r.recognize_google(audio)
    except sr.UnknownValueError:
            print('Could not Understand try again')
    Description=output
    Description.capitalize()
    patient=Patient.objects.all().first()
    prescription=Prescription(Doctor=request.user.doctor,patient=patient)
    prescription.Description=Description
    prescription.save()
    data={
        'flag':True
    }
    return render(request,'PrescriptionForm.html',data)








class DoctorComplaintView(ListView):
    model=Complaint
    template_name='DoctorComplaint.html'


def sendmail(request):
    send_mail(
    'test',
    'Hello.',
    EMAIL_HOST_USER,
    ['saivamshi.k.24@gmail.com'],
    fail_silently=False,
    )

def sendsms():
    client.send_message({
    'from': 'Health is Wealth',
    'to': '918639783590',
    'text': 'Your Prescritpion has been sent to your registered Mail.Thank you for using Health is Wealth',
})



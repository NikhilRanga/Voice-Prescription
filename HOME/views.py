from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import DoctorRegisterForm,ComplaintRegisterForm
from .models import Users,Doctor,Patient,Complaint,Prescription
from django import forms
from .utils import render_to_pdf
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import speech_recognition as sr
from VoicePrescription.settings import EMAIL_HOST_USER
import datetime
import nexmo
from VoicePrescription.settings import API_KEY,SECRET_KEY

client = nexmo.Client(key=API_KEY, secret=SECRET_KEY)

# Create your views here.
def HomePage(request):
    return render(request,'home.html',{})


def UserRegister(request):
    return render(request,'UserRegister.html')


def UserBlog(request):
    return render(request,'PatientBlog.html',{})


def patient_signup(request):
    doctors=Doctor.objects.all()
    if request.method=='POST':
        userform=UserRegisterForm(request.POST,prefix='userform')
        if userform.is_valid():
            user = userform.save()
            user.role = Users.PATIENT
            user.age = request.POST.get('Age')
            user.save()
            user1=Users.objects.get(username=request.POST.get('Doctor'))
            doctor=Doctor.objects.get(user=user1)
            patient = Patient(user=user,doctor=doctor)
            patient.save()
            username = userform.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('Login')
    else:
        userform = UserRegisterForm(prefix='userform')
        # patientform = PatientSignupForm(request.POST, prefix='patientform')
        return render(request=request, template_name='Patient_Signup.html',context={'form': userform,'doctors':doctors})


def doctor_signup(request):
    if request.method=='POST':
        userform=UserRegisterForm(request.POST,request.FILES,prefix='userform')
        if userform.is_valid():
                user = userform.save()
                user.role = Users.DOCTOR
                user.save()
                doctor=Doctor(user=user)
                doctor.Education=request.POST.get('Education')
                doctor.License=request.FILES.get('License')
                doctor.Specialization=request.POST.get('Specialization')
                doctor.AadharNo=request.POST.get('AadharNo')
                doctor.save()
                if ValueError:
                    user=Users.objects.all().last()
                    user.delete()
                username = userform.cleaned_data.get('username')
                messages.success(request,f'Account created for {username}')
                return redirect('Login')
        else:
            print(userform.errors)
    else:
        userform = UserRegisterForm(prefix='userform')
        context={'form': userform}
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
        r.adjust_for_ambient_noise(source)
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



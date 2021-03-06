from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import DoctorRegisterForm,ComplaintRegisterForm
from .models import Users,Doctor,Patient,Complaint,Prescription
from django import forms
from .utils import render_to_pdf
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
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

@login_required
def PatientProfile(request):
    user=Users.objects.get(id=request.user.id)
    patient=Patient.objects.get(user=user)
    return render(request,'PatientBlog.html',{'user':user,'patient':patient})

@login_required
def DoctorProfile(request):
    user=Users.objects.get(id=request.user.id)
    doctor=Doctor.objects.get(user=request.user)
    return render(request,'DoctorBlog.html',{'user':user,'doctor':doctor})


def patient_signup(request):
    doctors=Doctor.objects.all()
    if request.method=='POST':
        userform=UserRegisterForm(request.POST,prefix='userform')
        if userform.is_valid():
            user = userform.save()
            user.role = Users.PATIENT
            user.save()
            patient = Patient(user=user)
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
        doctorform=DoctorRegisterForm(request.POST,request.FILES,prefix='doctorform')
        if userform.is_valid() and doctorform.is_valid():
                user = userform.save(commit=False)
                user.role = Users.DOCTOR
                user.save()
                doctor=doctorform.save(commit=False)
                doctor.user=user
                doctor.save()
                username=userform.cleaned_data.get('username')
                messages.success(request,f'Account created for {username}')
                return redirect('Login')
        else:
            print(userform.errors)
    else:
        userform = UserRegisterForm(prefix='userform')
        doctorform=DoctorRegisterForm(prefix='doctorform')
        context={'form': userform,'dform':doctorform}
        return render(request,'Doctor_Signup.html',context)




@login_required
def GeneratePdf(request,primary_key):
    complaint=Complaint.objects.get(id=primary_key)
    prescription=Prescription.objects.get(complaint=complaint)
    doctor=complaint.Doctor
    DoctorName=doctor.user.username
    Description=prescription.Description
    Specialization=doctor.Specialization
    Date=prescription.Date
    image=doctor.Signature
    data = { 
        'DoctorName':DoctorName,
        'Date':Date,
        'Specialization': Specialization,
        'Description': Description,
        'image':image
    }
    pdf = render_to_pdf('Prescription.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required
def ComplaintRegistration(request):
    if request.method =='POST':
        complaintform=ComplaintRegisterForm(request.POST,prefix='complaintform')
        if complaintform.is_valid():
            complaint=complaintform.save(commit=False)
            complaint.patient=Patient.objects.get(user=request.user)
            user1=Users.objects.get(username=request.POST.get('Doctor'))
            doctor=Doctor.objects.get(user=user1)
            complaint.Doctor=doctor
            complaint.save()
            messages.success(request,f'Complaint Registered')
            return redirect('HomePage')
    else:
        Doctors=Doctor.objects.all()
        complaintform=ComplaintRegisterForm(prefix='complaintform')
        return render(request,'ComplaintRegistration.html',{'complaintform':complaintform,'Doctors':Doctors})

@login_required
def ComplaintListView(request):
    patient=Patient.objects.get(user=request.user)
    complaints=Complaint.objects.filter(patient=patient).values()
    template_name='ComplaintView.html'
    return render(request,template_name,context={'complaints':complaints})

@login_required
def ComplaintDetailView(request,id):
    complaint=Complaint.objects.get(id=id)
    return render(request,'ComplaintDetail.html',{'complaint':complaint})

@login_required
def DoctorComplaintDetailView(request,id):
    complaint=Complaint.objects.get(id=id)
    return render(request,'DoctorComplaintDetailView.html',{'complaint':complaint})


@login_required
def PrescriptionForm(request,primary_key):
    return render(request,'PrescriptionForm.html',{'primary_key':primary_key})

@login_required
def speech_to_text(request,primary_key):
    Description=request.POST.get('Description')
    r=sr.Recognizer()
    mic=sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio=r.record(source,duration=10)
    try:
        output = " " + r.recognize_google(audio)
    except sr.UnknownValueError:
        output = "Could not understand audio"
    except sr.RequestError as e:
        output = "Could not request results; {0}".format(e)   
    if(not Description):
        Description=output
    Description.capitalize()
    complaint=Complaint.objects.get(id=primary_key)
    patient=complaint.patient
    doctor=complaint.Doctor
    prescription=Prescription(Doctor=doctor,patient=patient)
    prescription.Description=Description
    prescription.complaint=complaint
    prescription.save()
    DoctorName=request.user.username
    Date=datetime.date.today
    doctor=Doctor.objects.get(user=request.user)
    prescription=Prescription.objects.get(complaint=complaint)
    Description=prescription.Description
    Specialization=prescription.Doctor.Specialization
    data = { 
        'DoctorName':DoctorName,
        'Date':Date,
        'Specialization': Specialization,
        'Description': Description
    }
    pdf = render_to_pdf('Prescription.html', data)
    subject='Prescription'
    from_=EMAIL_HOST_USER
    to=[patient.user.email]
    body='Prescription'
    email=EmailMultiAlternatives(subject,body,from_,to)
    email.attach('Prescription.pdf',pdf,'application/pdf')
    email.send()
    data={
        'flag':True,
        'primary_key':primary_key
    }
    return render(request,'PrescriptionForm.html',data)


def DoctorComplaintView(request):
    doctor=Doctor.objects.get(user=request.user)
    complaints=Complaint.objects.filter(Doctor=doctor).order_by('Date')
    template_name='DoctorComplaintView.html'
    return render(request,template_name,{"complaints":complaints,'doctor':doctor})



def sendsms():
    client.send_message({
    'from': 'Nexmo',
    'to': '918639783590',
    'text': 'Your Prescritpion has been sent to your registered Mail.\n Thank you for using Health is Wealth',
})
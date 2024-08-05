from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment, Patient, User
from .forms import PatientSignupForm, DoctorSignupForm, AppointmentForm

def signup(request):
    if request.method == 'POST':
        form_type = request.POST.get('user_type')
        if form_type == 'patient':
            form = PatientSignupForm(request.POST, request.FILES)
        elif form_type == 'doctor':
            form = DoctorSignupForm(request.POST, request.FILES)
        else:
            form = None  # Handle invalid form_type if needed
        if form is not None and form.is_valid():
            user = form.save(commit=False)
            if form_type == 'patient':
                user.is_patient = True
            elif form_type == 'doctor':
                user.is_doctor = True
            user.save()
            if user.is_patient:
                profile = Patient(user=user, address=form.cleaned_data['address'], profile_picture=form.cleaned_data['profile_picture'])
            elif user.is_doctor:
                profile = Doctor(user=user, address=form.cleaned_data['address'], profile_picture=form.cleaned_data['profile_picture'])
            profile.save()
            login(request, user)
            return redirect('doctor_list')  # Corrected name
    else:
        form = PatientSignupForm()
    return render(request, 'index.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('doctor_list')  # Corrected name
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_patient:
        profile = Patient.objects.get(user=request.user)
    elif request.user.is_doctor:
        profile = Doctor.objects.get(user=request.user)
    return render(request, 'dashboard.html', {'profile': profile})

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, user_id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user
            appointment.save()
            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_confirmation.html', {'appointment': appointment})

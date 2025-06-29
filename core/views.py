from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import ClinicProfile, Doctor, Testimonial, Treatment
from .forms import CustomUserCreationForm
from lectures.models import LectureRegistration

def home(request):
    clinic = ClinicProfile.objects.first()
    doctors = Doctor.objects.all()
    testimonials = Testimonial.objects.filter(is_approved=True)
    return render(request, 'core/home.html', {
        'clinic': clinic,
        'doctors': doctors,
        'testimonials': testimonials
    })

def about(request):
    clinic = ClinicProfile.objects.first()
    return render(request, 'core/about.html', {'clinic': clinic})

def services(request):
    clinic = ClinicProfile.objects.first()
    return render(request, 'core/services.html', {'clinic': clinic})

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def treatments(request):
    treatments = Treatment.objects.filter(is_active=True)
    return render(request, 'core/treatments.html', {'treatments': treatments})

@login_required
def dashboard(request):
    appointments = request.user.appointments.all()
    lecture_registrations = LectureRegistration.objects.filter(student=request.user)
    return render(request, 'core/dashboard.html', {
        'appointments': appointments,
        'lecture_registrations': lecture_registrations
    }) 
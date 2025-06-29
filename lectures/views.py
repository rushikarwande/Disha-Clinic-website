from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Lecture, LectureRegistration
from core.models import Doctor

def lecture_list(request):
    lectures = Lecture.objects.filter(date__gte=timezone.now().date()).order_by('date', 'start_time')
    return render(request, 'lectures/list.html', {'lectures': lectures})

@login_required
def create_lecture(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'You are not authorized to create lectures.')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        max_students = request.POST.get('max_students')

        lecture = Lecture.objects.create(
            title=title,
            description=description,
            doctor=request.user.doctor,
            date=date,
            start_time=start_time,
            end_time=end_time,
            max_students=max_students
        )
        messages.success(request, 'Lecture created successfully!')
        return redirect('lectures:list')
    
    return render(request, 'lectures/create.html')

@login_required
def register_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    
    if request.method == 'POST':
        # Check if user has already registered
        if LectureRegistration.objects.filter(lecture=lecture, student=request.user).exists():
            messages.error(request, 'You have already registered for this lecture.')
            return redirect('lectures:list')
        
        # Check if lecture is full
        if LectureRegistration.objects.filter(lecture=lecture, status='paid').count() >= lecture.max_students:
            messages.error(request, 'This lecture is full.')
            return redirect('lectures:list')
        
        # Create registration
        registration = LectureRegistration.objects.create(
            lecture=lecture,
            student=request.user
        )
        return redirect('lectures:payment', lecture_id=lecture.id)
    
    return render(request, 'lectures/register.html', {'lecture': lecture})

@login_required
def lecture_payment(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    registration = get_object_or_404(LectureRegistration, lecture=lecture, student=request.user)
    
    if request.method == 'POST':
        # Here you would integrate with your payment gateway
        # For now, we'll just mark it as paid
        registration.status = 'paid'
        registration.payment_id = 'test_payment_id'  # Replace with actual payment ID
        registration.save()
        messages.success(request, 'Payment successful!')
        return redirect('lectures:payment_success', lecture_id=lecture.id)
    
    return render(request, 'lectures/payment.html', {
        'lecture': lecture,
        'registration': registration
    })

@login_required
def payment_success(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    registration = get_object_or_404(LectureRegistration, lecture=lecture, student=request.user)
    return render(request, 'lectures/payment_success.html', {
        'lecture': lecture,
        'registration': registration
    })

@login_required
def my_registrations(request):
    registrations = LectureRegistration.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'lectures/my_registrations.html', {'registrations': registrations}) 
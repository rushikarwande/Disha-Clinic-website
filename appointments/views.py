from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Appointment, TimeSlot
from core.models import Doctor

@login_required
def book_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time_slot_id = request.POST.get('time_slot')
        reason = request.POST.get('reason')
        patient_name = request.POST.get('patient_name')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        time_slot = get_object_or_404(TimeSlot, id=time_slot_id)

        # Check if the time slot is still available
        if not time_slot.is_available:
            messages.error(request, 'This time slot is no longer available. Please select another slot.')
            return redirect('appointments:book_appointment')

        # Check if the user already has an appointment at this time
        existing_appointment = Appointment.objects.filter(
            Q(patient=request.user) & 
            Q(time_slot__date=time_slot.date) & 
            Q(time_slot__start_time=time_slot.start_time) &
            ~Q(status__in=['cancelled', 'rejected'])
        ).first()

        if existing_appointment:
            messages.error(request, 'You already have an appointment at this time.')
            return redirect('appointments:book_appointment')

        # Create the appointment with pending status
        appointment = Appointment.objects.create(
            patient=request.user,
            patient_name=patient_name,
            doctor=doctor,
            time_slot=time_slot,
            reason=reason,
            status='pending'
        )
        
        messages.success(request, 'Appointment request submitted successfully! Please wait for doctor\'s approval.')
        return redirect('appointments:my_appointments')
    
    # Get available doctors
    doctors = Doctor.objects.filter(is_available=True)
    
    # Get available time slots
    available_slots = TimeSlot.objects.filter(
        is_available=True,
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')
    
    # Group time slots by date for better organization
    time_slots_by_date = {}
    for slot in available_slots:
        date_str = slot.date.strftime('%Y-%m-%d')
        if date_str not in time_slots_by_date:
            time_slots_by_date[date_str] = []
        time_slots_by_date[date_str].append(slot)
    
    return render(request, 'appointments/book.html', {
        'doctors': doctors,
        'available_slots': available_slots,
        'time_slots_by_date': time_slots_by_date,
        'today': timezone.now().date()
    })

@login_required
def my_appointments(request):
    # Get all appointments for the current user
    appointments = Appointment.objects.filter(patient=request.user).order_by('-created_at')
    
    # Separate appointments by status
    pending_appointments = appointments.filter(status='pending')
    approved_appointments = appointments.filter(status='approved')
    completed_appointments = appointments.filter(status='completed')
    cancelled_appointments = appointments.filter(status__in=['cancelled', 'rejected'])
    
    return render(request, 'appointments/my_appointments.html', {
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments
    })

@login_required
def doctor_appointments(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')
    
    # Get all appointments for the current doctor
    appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('-created_at')
    
    # Separate appointments by status
    pending_appointments = appointments.filter(status='pending')
    approved_appointments = appointments.filter(status='approved')
    completed_appointments = appointments.filter(status='completed')
    cancelled_appointments = appointments.filter(status__in=['cancelled', 'rejected'])
    
    return render(request, 'appointments/doctor_appointments.html', {
        'pending_appointments': pending_appointments,
        'approved_appointments': approved_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments
    })

@login_required
def approve_appointment(request, appointment_id):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        response = request.POST.get('response', '')
        
        if action == 'approve':
            appointment.status = 'approved'
            appointment.doctor_response = response
            messages.success(request, 'Appointment approved successfully!')
        elif action == 'reject':
            appointment.status = 'rejected'
            appointment.doctor_response = response
            messages.success(request, 'Appointment rejected.')
        
        appointment.save()
    
    return redirect('appointments:doctor_appointments')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.user == appointment.patient or request.user == appointment.doctor.user:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
        
        if request.user == appointment.patient:
            return redirect('appointments:my_appointments')
        else:
            return redirect('appointments:doctor_appointments')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('home')

@login_required
def complete_appointment(request, appointment_id):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
    appointment.status = 'completed'
    appointment.save()
    messages.success(request, 'Appointment marked as completed!')
    return redirect('appointments:doctor_appointments') 
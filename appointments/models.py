from django.db import models
from django.contrib.auth.models import User
from core.models import Doctor

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.start_time} to {self.end_time}"

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['date', 'start_time', 'end_time']

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Payment Pending'),
        ('paid', 'Payment Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=100, help_text="Name of the patient for the appointment", null=True, blank=True)
    doctor = models.ForeignKey('core.Doctor', on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    doctor_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient_name or self.patient.get_full_name()} with Dr. {self.doctor.user.get_full_name()} on {self.time_slot.date}"

    class Meta:
        ordering = ['-time_slot__date', '-time_slot__start_time']

    @property
    def date(self):
        return self.time_slot.date

    def save(self, *args, **kwargs):
        # If appointment is approved, make the time slot unavailable
        if self.status == 'approved' and self._state.adding:
            self.time_slot.is_available = False
            self.time_slot.save()
        # If appointment is cancelled or rejected, make the time slot available again
        elif self.status in ['cancelled', 'rejected']:
            self.time_slot.is_available = True
            self.time_slot.save()
        super().save(*args, **kwargs) 
from django.db import models
from django.contrib.auth.models import User

class ClinicProfile(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='clinic_logos/', null=True, blank=True)
    about_us = models.TextField()
    services = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Treatment(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Health'),
        ('women', 'Women\'s Health'),
        ('skin', 'Skin & Hair'),
        ('digestive', 'Digestive System'),
        ('respiratory', 'Respiratory System'),
        ('musculoskeletal', 'Musculoskeletal System'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='treatments/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']

class Testimonial(models.Model):
    patient_name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Testimonial by {self.patient_name}" 
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel'),
    path('complete/<int:appointment_id>/', views.complete_appointment, name='complete'),
] 
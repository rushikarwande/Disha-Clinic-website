from django.urls import path
from . import views

app_name = 'lectures'

urlpatterns = [
    path('', views.lecture_list, name='list'),
    path('create/', views.create_lecture, name='create'),
    path('register/<int:lecture_id>/', views.register_lecture, name='register'),
    path('payment/<int:lecture_id>/', views.lecture_payment, name='payment'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('success/<int:lecture_id>/', views.payment_success, name='payment_success'),
] 
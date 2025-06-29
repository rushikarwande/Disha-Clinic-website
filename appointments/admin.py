from django.contrib import admin
from .models import TimeSlot, Appointment

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'is_available')
    list_filter = ('date', 'is_available')
    search_fields = ('date',)
    fieldsets = (
        ('Time Slot Details', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Availability', {
            'fields': ('is_available',)
        })
    )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient', 'doctor', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'time_slot__date')
    search_fields = ('patient_name', 'patient__username', 'patient__first_name', 'patient__last_name',
                    'doctor__user__username', 'doctor__user__first_name', 'doctor__user__last_name')
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'patient_name', 'doctor', 'time_slot', 'reason')
        }),
        ('Status', {
            'fields': ('status', 'doctor_response')
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_amount', 'payment_id')
        })
    )
    actions = ['approve_appointments', 'cancel_appointments']

    def approve_appointments(self, request, queryset):
        queryset.update(status='approved')
    approve_appointments.short_description = "Approve selected appointments"

    def cancel_appointments(self, request, queryset):
        queryset.update(status='cancelled')
        # Make time slots available again
        for appointment in queryset:
            appointment.time_slot.is_available = True
            appointment.time_slot.save()
    cancel_appointments.short_description = "Cancel selected appointments" 
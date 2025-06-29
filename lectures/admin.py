from django.contrib import admin
from .models import Lecture, LectureRegistration

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'doctor', 'date', 'start_time', 'end_time', 'max_students', 'meet_link')
    list_filter = ('date', 'doctor')
    search_fields = ('title', 'description', 'doctor__user__username', 'doctor__user__first_name', 'doctor__user__last_name')
    fieldsets = (
        ('Lecture Details', {
            'fields': ('title', 'description', 'doctor')
        }),
        ('Schedule', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Capacity and Link', {
            'fields': ('max_students', 'meet_link'),
            'description': 'Add the meeting link (e.g., Zoom, Google Meet) for the lecture'
        })
    )

@admin.register(LectureRegistration)
class LectureRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'lecture', 'status', 'payment_id', 'created_at')
    list_filter = ('status', 'lecture__date')
    search_fields = ('student__username', 'student__first_name', 'student__last_name',
                    'lecture__title', 'payment_id')
    fieldsets = (
        ('Registration Details', {
            'fields': ('student', 'lecture')
        }),
        ('Payment Information', {
            'fields': ('status', 'payment_id', 'payment_amount')
        })
    )
    actions = ['mark_as_paid', 'mark_as_cancelled']

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_as_paid.short_description = "Mark selected registrations as paid"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected registrations as cancelled" 
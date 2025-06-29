from django.contrib import admin
from .models import ClinicProfile, Doctor, Testimonial, Treatment

@admin.register(ClinicProfile)
class ClinicProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience', 'is_available')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')
    list_filter = ('specialization', 'is_available')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'rating', 'is_approved', 'created_at')
    search_fields = ('patient_name', 'content')
    list_filter = ('is_approved', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'image_tag', 'created_at')
    search_fields = ('name', 'category', 'description')
    list_filter = ('category', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 60px; max-width: 60px;" />'
        return "-"
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True 
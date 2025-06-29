from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import ClinicProfile, Doctor, Testimonial

class Command(BaseCommand):
    help = 'Sets up initial data for the clinic'

    def handle(self, *args, **kwargs):
        # Create clinic profile
        clinic, created = ClinicProfile.objects.get_or_create(
            name="Disha Homopathy Clinic",
            defaults={
                'description': "A leading homoeopathic clinic providing holistic healthcare solutions.",
                'address': "123 Main Street, City, State, Country",
                'phone': "+1234567890",
                'email': "contact@dishaclinic.com",
                'about_us': "We are committed to providing the best homoeopathic care to our patients.",
                'services': "Online Consultations, Practical Lectures, Holistic Treatment"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created clinic profile'))

        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dishaclinic.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create doctor user and profile
        doctor_user, created = User.objects.get_or_create(
            username='doctor',
            defaults={
                'email': 'doctor@dishaclinic.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'is_staff': True
            }
        )
        if created:
            doctor_user.set_password('doctor123')
            doctor_user.save()
            self.stdout.write(self.style.SUCCESS('Created doctor user'))

        doctor, created = Doctor.objects.get_or_create(
            user=doctor_user,
            defaults={
                'specialization': 'General Homoeopathy',
                'experience': 10,
                'bio': 'Experienced homoeopathic doctor with expertise in treating various conditions.',
                'is_available': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created doctor profile'))

        # Create sample testimonials
        testimonials = [
            {
                'patient_name': 'Alice Smith',
                'content': 'Excellent treatment and care. The doctor was very knowledgeable and helpful.',
                'rating': 5,
                'is_approved': True
            },
            {
                'patient_name': 'Bob Johnson',
                'content': 'Great experience with the online consultation. Very convenient and effective.',
                'rating': 4,
                'is_approved': True
            },
            {
                'patient_name': 'Carol White',
                'content': 'The holistic approach to treatment has helped me a lot. Highly recommended!',
                'rating': 5,
                'is_approved': True
            }
        ]

        for testimonial_data in testimonials:
            testimonial, created = Testimonial.objects.get_or_create(
                patient_name=testimonial_data['patient_name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created testimonial for {testimonial_data["patient_name"]}')) 
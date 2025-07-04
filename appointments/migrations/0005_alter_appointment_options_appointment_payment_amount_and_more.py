# Generated by Django 5.0.7 on 2025-06-10 13:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_appointment_doctor_response_alter_appointment_status'),
        ('core', '0002_treatment_testimonial_updated_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['-time_slot__date', '-time_slot__start_time']},
        ),
        migrations.AddField(
            model_name='appointment',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, default=300.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='appointment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Payment Pending'), ('paid', 'Payment Completed')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='core.doctor'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor_response',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Approval'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.timeslot'),
        ),
    ]

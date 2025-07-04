# Generated by Django 5.0.7 on 2025-06-10 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('general', 'General Health'), ('women', "Women's Health"), ('skin', 'Skin & Hair'), ('digestive', 'Digestive System'), ('respiratory', 'Respiratory System'), ('musculoskeletal', 'Musculoskeletal System')], max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='treatments/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['category', 'name'],
            },
        ),
        migrations.AddField(
            model_name='testimonial',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

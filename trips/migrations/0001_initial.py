# Generated by Django 5.1.4 on 2025-03-16 11:10

import cloudinary.models
import django.core.validators
import django.db.models.deletion
import trips.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('place', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('country', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(56)])),
                ('content', models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(500)])),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('trip_category', models.CharField(choices=[('Leisure', 'LEISURE'), ('Business', 'BUSINESS'), ('Adventure', 'ADVENTURE'), ('Family', 'FAMILY'), ('Romantic', 'ROMANTIC')], default='LEISURE', max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('trip_status', models.CharField(choices=[('Completed', 'COMPLETED'), ('Ongoing', 'ONGOING'), ('Planned', 'PLANNED')], default='PLANNED', max_length=50)),
                ('shared', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', 'country', 'start_date'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_title', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('image', cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/dchoskzxj/image/upload/v1721990160/yg9qwd4v15r23bxwv5u4.jpg', max_length=255, null=True, validators=[trips.utils.validate_image], verbose_name='image')),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(500)])),
                ('shared', models.BooleanField(default=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='trips.trip')),
            ],
            options={
                'ordering': ['-uploaded_at', 'owner'],
            },
        ),
    ]

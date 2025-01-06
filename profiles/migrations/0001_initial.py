# Generated by Django 5.1.4 on 2025-01-06 13:41

import cloudinary.models
import django.db.models.deletion
import profiles.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('alias', models.CharField(blank=True, max_length=50)),
                ('content', models.TextField(blank=True)),
                ('image', cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/dchoskzxj/image/upload/v1721990160/yg9qwd4v15r23bxwv5u4.jpg', max_length=255, null=True, validators=[profiles.models.validate_image], verbose_name='image')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

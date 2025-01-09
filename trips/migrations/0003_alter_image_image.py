# Generated by Django 5.1.4 on 2025-01-09 16:50

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_alter_trip_shared'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dchoskzxj/image/upload/v1721990160/yg9qwd4v15r23bxwv5u4.jpg', max_length=255, verbose_name='image'),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-17 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0004_profile_image_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image_url',
        ),
    ]

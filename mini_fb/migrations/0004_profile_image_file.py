# Generated by Django 5.1.2 on 2024-10-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_statusmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image_file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]

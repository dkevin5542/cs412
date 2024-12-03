# Generated by Django 5.1.3 on 2024-12-03 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0012_remove_merchandise_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the audio file', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Description of the audio file', null=True)),
                ('file', models.FileField(help_text='Upload MP3 file', upload_to='audio/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, help_text='Date and time the file was uploaded')),
            ],
        ),
    ]
# Generated by Django 5.1.3 on 2024-11-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('synopsis', models.TextField(blank=True, null=True)),
                ('genre', models.TextField()),
                ('aired', models.CharField(max_length=255)),
                ('episodes', models.PositiveIntegerField(blank=True, null=True)),
                ('members', models.PositiveIntegerField()),
                ('popularity', models.PositiveIntegerField()),
                ('ranked', models.FloatField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('img_url', models.URLField(blank=True, null=True)),
                ('link', models.URLField()),
            ],
        ),
    ]

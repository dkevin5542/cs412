# Generated by Django 5.1.3 on 2024-11-22 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0005_character'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_anime',
            field=models.ManyToManyField(blank=True, help_text='Select your favorite anime.', related_name='favorited_by', to='final_project.anime'),
        ),
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('figurine', 'Figurine'), ('poster', 'Poster'), ('apparel', 'Apparel'), ('accessory', 'Accessory'), ('other', 'Other')], default='other', max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchandise', to='final_project.character')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchandise', to='final_project.user')),
            ],
        ),
    ]
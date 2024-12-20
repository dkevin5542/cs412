# Generated by Django 5.1.3 on 2024-11-22 17:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0007_user_selected_merchandise'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_user',
            field=models.ForeignKey(default=1, help_text='The associated Django auth user.', on_delete=django.db.models.deletion.CASCADE, related_name='custom_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('auth_user',), name='unique_auth_user_constraint'),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-22 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_project', '0002_anime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime',
            old_name='score',
            new_name='rating',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='aired',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='id',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='img_url',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='link',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='uid',
        ),
        migrations.AddField(
            model_name='anime',
            name='mal_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='anime',
            name='source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='studio',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='type',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='anime',
            name='episodes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='anime',
            name='genre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='anime',
            name='members',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='anime',
            name='popularity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='anime',
            name='ranked',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

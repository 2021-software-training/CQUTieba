# Generated by Django 3.2.5 on 2021-07-15 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0008_auto_20210716_0333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='audio_person',
        ),
        migrations.RemoveField(
            model_name='article',
            name='audio_pitch',
        ),
        migrations.RemoveField(
            model_name='article',
            name='audio_speed',
        ),
        migrations.RemoveField(
            model_name='article',
            name='audio_volume',
        ),
    ]

# Generated by Django 3.2.5 on 2021-07-15 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_myuser_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='photo_url',
        ),
    ]

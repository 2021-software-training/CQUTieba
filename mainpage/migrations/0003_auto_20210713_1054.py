# Generated by Django 3.2.5 on 2021-07-13 02:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_article_article_chose_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_to',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 2, 54, 4, 333156, tzinfo=utc)),
        ),
    ]

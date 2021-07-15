# Generated by Django 3.2.5 on 2021-07-15 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_auto_20210715_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('audio', models.FileField(upload_to='audio')),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='article_audio',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
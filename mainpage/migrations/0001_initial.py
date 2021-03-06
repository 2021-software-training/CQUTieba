# Generated by Django 3.2.5 on 2021-07-10 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('author_id', models.PositiveIntegerField()),
                ('article_text', models.TextField(max_length=20000)),
                ('article_views', models.IntegerField(default=0)),
                ('article_time', models.DateTimeField(auto_now_add=True)),
                ('article_audio', models.FileField(blank=True, upload_to='')),
                ('article_title', models.CharField(max_length=15)),
                ('likes_num', models.PositiveIntegerField(default=0)),
                ('comments_num', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=500)),
                ('commenter_id', models.PositiveIntegerField()),
                ('article_id', models.PositiveIntegerField()),
                ('likes_num', models.PositiveIntegerField()),
                ('comment_audio', models.FileField(upload_to='')),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LikeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]

import django.utils.timezone
from django.db import models
# Create your models here.
from mainpage.audio import *
from django.db import models
# Create your models here.
from django.utils import timezone as django_tz

class Article(models.Model):
    article_id = models.PositiveIntegerField(primary_key=True)
    author_id = models.PositiveIntegerField()

    article_text = models.TextField(max_length=20000)
    article_views = models.IntegerField(default=0)
    article_time = models.DateTimeField(default=django_tz.now)

    article_audio = models.FileField(blank=True)
    article_title = models.CharField(max_length=15)
    article_chose_audio=models.BooleanField(default=True)  #是否选择要上传声纹信息
    likes_num = models.PositiveIntegerField(default=0)
    comments_num = models.PositiveIntegerField(default=0)

    article_type1 = models.CharField(blank=True, max_length=10)
    article_type2 = models.CharField(blank=True, max_length=10)
    article_type3 = models.CharField(blank=True, max_length=10)

    w = models.FloatField(default = 0)#文章的权值

    @property
    def regist_time(self):#求出所差的时间(小时)
        delta = django_tz.now() - self.article_time
        return delta.days*24 + delta.seconds//3600



class Comment(models.Model):
    comment_id = models.PositiveIntegerField(primary_key=True)
    comment_text = models.TextField(max_length=500)
    commenter_id = models.PositiveIntegerField()
    article_id = models.PositiveIntegerField()
    likes_num = models.PositiveIntegerField(default=0)
    comment_audio = models.FileField(blank=True)
    comment_time = models.DateTimeField(default=django_tz.now)
    comment_to = models.BooleanField(default=True)
    #评论是指向何方，article:1,comment:0
    class Meta:
        ordering = ['comment_time']

    def __str__(self):
        return str(self.article_id) + ": " + str(self.commenter_id)


class LikeList(models.Model):
    """
    用于存储 文章 <--> 点赞用户id，用于判断是否改文章是否被访问用户点赞过
    """
    article_id = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.article_id) + ": " + str(self.user_id)


class LikeListComment(models.Model):
    """
    用于存储 文章 <--> 点赞用户id，用于判断是否改文章是否被访问用户点赞过
    """
    comment_id = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return str(self.comment_id) + ": " + str(self.user_id)

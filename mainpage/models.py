from django.db import models
from login.models import MyUser
# Create your models here.
from mainpage.audio import *
from django.utils import timezone
class Article(models.Model):
    article_id = models.PositiveIntegerField(primary_key=True)
    author_id = models.PositiveIntegerField()

    article_text = models.TextField(max_length=20000)
    article_views = models.IntegerField(default=0)
    article_time = models.DateTimeField(default = timezone.now())

    article_chose_audio = models.BooleanField(default=True)#是否选择要上传声纹信息
    article_audio = models.FileField(blank=True)#upload_to='D:\djanggo_pros\CQUTieba-branch2\mainpage')#声纹信息

    article_title = models.CharField(max_length=15)

    likes_num = models.PositiveIntegerField(default=0)
    comments_num = models.PositiveIntegerField(default=0)

    article_type1 = models.CharField(blank=True, max_length=10)
    article_type2 = models.CharField(blank=True, max_length=10)
    article_type3 = models.CharField(blank=True, max_length=10)


class Comment(models.Model):
    comment_text = models.TextField(max_length=500)#评论本身
    commenter_id = models.PositiveIntegerField()#评论的是谁
    article_id = models.PositiveIntegerField()#评论的文章
    likes_num = models.PositiveIntegerField(default=0)#点赞数
    comment_audio = models.FileField(blank=True)#语音信息
    comment_time = models.DateTimeField(auto_now_add=True)#评论时间


class LikeList(models.Model):#点赞表格
    """
    用于存储 文章 <--> 点赞用户id，用于判断是否改文章是否被访问用户点赞过
    """
    article_id = models.IntegerField()
    user_id = models.IntegerField()

from django.db import models
from login.models import MyUser
# Create your models here.


class Article(models.Model):
    article_id = models.PositiveIntegerField(primary_key=True)
    author_id = models.PositiveIntegerField()

    article_text = models.TextField(max_length=20000)
    article_views = models.IntegerField(default=0)
    article_time = models.DateTimeField(auto_now_add=True)

    article_audio = models.FileField(blank=True)
    article_title = models.CharField(max_length=15)

    likes_num = models.PositiveIntegerField(default=0)
    comments_num = models.PositiveIntegerField(default=0)

    article_type1 = models.CharField(blank=True, max_length=10)
    article_type2 = models.CharField(blank=True, max_length=10)
    article_type3 = models.CharField(blank=True, max_length=10)

    def __str__(self):
        return self.article_title


class Comment(models.Model):
    comment_id = models.PositiveIntegerField(default=0, primary_key=True)
    comment_text = models.TextField(max_length=500)
    commenter_id = models.PositiveIntegerField()
    article_id = models.PositiveIntegerField()
    likes_num = models.PositiveIntegerField(default=0)
    comment_audio = models.FileField(blank=True)
    comment_time = models.DateTimeField(auto_now_add=True)

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


class Image(models.Model):
    """
    用于存储图片
    """
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='img', blank=False)

    def __str__(self):
        return str(self.id)
from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    my_user_id = models.PositiveIntegerField(primary_key=True)
    
    age = models.PositiveSmallIntegerField(default=0)
    gender = models.PositiveSmallIntegerField(default=0)    # 1: 男性，2：女性，0：未设定

    # profile = models.FileField(upload_to="profile", blank=True)
    profile = models.IntegerField(default=0)    # 保存图片ID

    address_provinces = models.CharField(blank=True, max_length=10)
    address_city = models.CharField(blank=True, max_length=10)

    habits1 = models.CharField(blank=True, max_length=10)
    habits2 = models.CharField(blank=True, max_length=10)
    habits3 = models.CharField(blank=True, max_length=10)

    status = models.BooleanField(default=True)
    signature = models.CharField(default='还没有个性签名呢~', max_length=50)
    exp_value = models.PositiveIntegerField(default=1)

    font_size = models.IntegerField(default=10)

    def __str__(self):
        return self.user.username


class NumCounter(models.Model):
    counter_id = models.IntegerField(primary_key=True)
    my_user_id = models.PositiveIntegerField(default=100000)
    my_article_id = models.PositiveIntegerField(default=1100000)

    def __str__(self):
        return str(self.counter_id)

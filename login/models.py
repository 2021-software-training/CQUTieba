from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    age = models.PositiveSmallIntegerField(default=1)        # PositiveSmallIntegerField
    gender = models.PositiveSmallIntegerField(default=3)
    photo_url = models.ImageField(blank=True)

    address_provinces = models.CharField(blank=True)
    address_city = models.CharField(blank=True)

    habits1 = models.CharField(blank=True)
    habits2 = models.CharField(blank=True)
    habits3 = models.CharField(blank=True)

    birthday = models.DateTimeField(blank=True)
    status = models.BooleanField(default=True)
    signature = models.CharField(default='还没有个性签名呢~')
    exp_value = models.PositiveIntegerField(default=1)

    front_size = models.IntegerField(default=10)

    def __str__(self):
        return self.user.username

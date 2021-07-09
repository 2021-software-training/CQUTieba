from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MyUser(User):
    sexy = models.BooleanField()
    age = models.IntegerField()
    photo_url = models.ImageField()
    login_time = models.DateTimeField()

    def __str__(self):
        return self.username


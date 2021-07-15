from django.contrib import admin
from login.models import MyUser, NumCounter

admin.site.register(MyUser)
admin.site.register(NumCounter)
# Register your models here.

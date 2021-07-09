from django.db import models
from datetime import  datetime
# Create your models here.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'pro2.settings'
class EmailVerifyRecord(models.Model):#邮箱类别
    """
    图形验证码
    """
    send_choices = (
        ('register','注册'),
        ('forget','找回密码')
    )
    code = models.CharField('验证码',max_length=20)
    email = models.EmailField('邮箱',max_length=50)
    send_type = models.CharField(choices=send_choices,max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return  '{0}({1})'.format(self.code, self.email)

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from random import Random
from django.core.mail import send_mail
from django.conf import settings
from CQUTieba.settings import EMAIL_FROM
from django.core.cache import cache

from datetime import datetime

TIME_OUT = 5 * 60


class EmailVerifyRecord:  # 邮箱类别
    def __init__(self, code='a', email="b", send_choice="regist", send_time=datetime.now()):
        self.code = code  # 验证码
        self.email = email  # 邮箱地址
        self.send_choice = send_choice  # 发送的需求
        self.send_time = send_time  # 注册的时间

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


def random_str(random_length=5):
    """
    :param random_length:
    :return:
    """
    # 字符串验证
    string = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        string += chars[random.randint(0, length)]
    return string


def send_register_email(email):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    code = random_str(5)
    email_record.code = code
    email_record.email = email
    # email_record.save(),这个功能在完成全部注册后和其他进行合并
    # 定义邮件内容:
    email_title = ""
    email_body = ""

    email_title = "django - 注册激活链接"
    email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/email/{0}\n" \
                 "该链接3分钟后失效".format(code)
    # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    # 如果发送成功
    cache.set(email, code, TIME_OUT)


def user_check(name: str, ps: str) -> bool:
    """
    判断是否用户名与密码一致
    当用户不存在或者用户名与密码不一致的时候，返回False
    否则返回True
    """
    try:
        user = User.objects.get(username=name)
        return check_password(ps, user.password)
    except User.DoesNotExist:
        return False

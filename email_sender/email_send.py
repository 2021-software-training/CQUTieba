from random import Random
from django.core.mail import  send_mail
from email_sender.util import EmailVerifyRecord
from django.conf import  settings
from CQUTieba.settings import EMAIL_FROM
from django.http import HttpResponse, HttpResponseRedirect
def check_email(email_address):
    return True
def random_str(random_length=5):
    #字符串验证
    str=''
    chars= 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length=len(chars)-1
    random=Random()
    for i in range(random_length):
        str+=chars[random.randint(0,length)]
    return str
#随机生成字符串
def send_register_email(email,send_type="regist"):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record=EmailVerifyRecord()
    # 生成随机的code放入链接
    code=random_str(5)
    email_record.code=code
    email_record.email=email
    #email_record.save(),这个功能在完成全部注册后和其他进行合并
    # 定义邮件内容:
    email_title=""
    email_body=""
    if send_type=="regist":
        email_title="django - 注册激活链接"
        email_body="请点击下面的链接激活你的账号: http://127.0.0.1:8000/email_sender/{0}\n" \
                   "该链接3分钟后失效".format(code)
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        # 如果发送成功
        if send_status:
            pass
    if send_type=="forget":
        email_title="django - 找回密码"
        email_body="请点击下面的链接找回你的密码: http://127.0.0.1:8000/email_sender/{0}\n" \
                   "该链接3分钟后失效".format(code)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        # 如果发送成功
        if send_status:
            pass
    return HttpResponse({"code":code})#发送给邮箱操作页面
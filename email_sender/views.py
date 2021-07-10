from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from email_sender.util import EmailVerifyRecord#工具库引入
from email_sender.email_send import *
def email_dir(request):#导引函数，填写邮箱之后会跳转
    email_address=request.GET(['email_address'])#前端抓取信息
    send_method=request.method#发送的信息类别
    if(check_email(email_address)):# 如果邮箱存在
        if(send_method=="regist"):
            send_method="注册"
            send_register_email(email_address,send_type="regist")#发送邮箱
        elif(send_method=="forget"):
            send_method="找回"
            send_register_email(email_address,send_type="forget")#发送邮箱
        return HttpResponse("邮箱操作方式%s"%(send_method))
    else:
        return HttpResponse("该邮箱已经存在,请重新来过")
def email_op(request,code):#邮箱操作的函数,发送邮箱之后激活
    return HttpResponse('你的邮箱验证码<br> <h1>{0}</h1>'.format(code))
#测试完毕






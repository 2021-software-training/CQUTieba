from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from register.models import EmailVerifyRecord
from email_send import random_str
def main(request):
    return HttpResponse("register")
# Create your views here.
def main1(request):
    return render(request,'reg_index.html')
def register(request):
    username,password,age=request.GET(['username']),request.GET(['password']),request.GET(['age'])
    sex,CAPTCHA=request.GET(['sex']),request.GET(['CAPTCHA'])
    #抓取信息
class ActiveUserView(View):
    def get(self,request,active_code):
        all_record=EmailVerifyRecord.objects.filter(code=active_code)
        if(all_record):
            for record in all_record:
                email=record.email
        else:
            return HttpResponse("激活失败")
        #转到激活失败
        return HttpResponse("激活成功")



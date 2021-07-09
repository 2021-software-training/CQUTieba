from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from login.utils import user_check
import json

from login.token import check_token, create_token

# Create your views here.


def register(request):
    if request.method == "POST":
        register_username = request.POST['username']

        # 获得用户名之后进行判断是否已经被注册
        registrant = authenticate(username=register_username)
        if registrant is not None:
            return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')
        else:
            register_password = request.POST['password']
            # register_email = request.POST['email']
            userinfo = {"username": register_username, "password": register_password}
            user = User.objects.create_user(**userinfo)
            user.save()
            return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')
    return HttpResponse(json.dumps({"result": "not json"}), content_type='application/json')


def login(request):
    if request.method == "GET":
        username = request.GET['username']
        password = request.GET['password']

        print("login_username: ", username, "\tlogin_password: ", password)

        if not user_check(name=username, ps=password):
            return HttpResponse(
                json.dumps({"result": "no", "token": "none", "name": username, "password": password}),
                content_type='application/json'
            )
        else:
            token = create_token(username)
            return HttpResponse(
                json.dumps({"result": "yes", "token": token}),
                content_type='application/json'
            )
    return HttpResponse("not post")


def func1(request):
    if request.GET["judge"] == "1":
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def func2(request):
    if request.POST["judge"] == "1":
        return HttpResponse("yes")
    else:
        return HttpResponse("no")


def return_json(request):
    data = {"judge": 'yes'}
    return HttpResponse(json.dumps(data), content_type='application/json')

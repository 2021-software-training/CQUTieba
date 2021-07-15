from django.contrib.auth.models import User
from login.models import MyUser, NumCounter
from django.http import HttpResponse, JsonResponse
from login.utils import user_check
import json

from login.token import check_token, create_token


# Create your views here.
from mainpage.utils import user_authentication


def register(request):
    print(1)
    if request.method == "GET":
        print(request.GET)
        register_username = request.GET['username']
        try:
            # 用户名已经存在
            MyUser.objects.get(user__username=register_username)
            return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')
        except MyUser.DoesNotExist:
            register_password = request.GET['password']
            register_email = request.GET['email']
            register_age = request.GET['age']
            # register_sex = request.GET['sex']
            userinfo = {
                "username": register_username,
                "password": register_password,
                "email": register_email,
            }
            User.objects.create_user(**userinfo)
            user = User.objects.get(username=register_username)
            counter = NumCounter.objects.get(pk=1)
            my_user = MyUser(user=user, age=register_age, my_user_id=counter.my_user_id)
            counter.my_user_id += 1
            user.save()
            my_user.save()
            counter.save()
            return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')
    return HttpResponse(json.dumps({"result": "not json"}), content_type='application/json')


def login(request):
    if request.method == "GET":
        username = request.GET['username']
        password = request.GET['password']

        print("login_username: ", username, "\tlogin_password: ", password)

        if user_check(name=username, ps=password):
            token = create_token(username)
            return HttpResponse(
                json.dumps({"result": "yes", "token": token}),
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps({"result": "no", "token": "none", "name": username, "password": password}),
                content_type='application/json'
            )
    return HttpResponse("not post")


def return_json(request):
    data = {"judge": 'yes'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def update_password(request):
    """
    更新密码
    :param request:
    :return:
    """
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    username = res['username']
    user = MyUser.objects.get(user__username=username)

    old_password = request.GET["oldPassword"]
    new_password = request.GET["newPassword"]
    if user_check(name=username, ps=old_password):
        user.user.set_password(new_password)
        user.user.save()
        user.save()
        return JsonResponse({"result": "yes"})

    return JsonResponse({"result": "no"})


def face_recognition(request):
    """

    :param request:
    :return:
    """

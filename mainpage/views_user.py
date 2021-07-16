import json
from django.http import HttpResponse, JsonResponse
from login.models import MyUser
from mainpage.utils import user_authentication
from mainpage.models import *


def get_userinfo(request):
    """
    获得用户的基本个人信息，
    :param request: {
        userID: my_user_id
    }
    :return
    """
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        my_username = request.GET['username']
        data = {}
        try:
            my_user = MyUser.objects.get(user__username=my_username)
            data["userID"] = my_user.my_user_id
            data["username"] = my_username
            data["email"] = my_user.user.email
            data["gender"] = my_user.gender
            data["age"] = my_user.age

            data["addressProvinces"] = my_user.address_provinces
            data["addressCity"] = my_user.address_city

            data["habits1"] = my_user.habits1
            data["habits2"] = my_user.habits2
            data["habits3"] = my_user.habits3
            data["signature"] = my_user.signature
            data["expValue"] = my_user.exp_value
            data["frontSize"] = my_user.front_size
            # data["photo"] =
        except MyUser.DoesNotExist:
            data = {"result": "no"}

        return JsonResponse(data=data)


def edit_userinfo(request):
    """
    编辑用户的个人信息
    :param request:{
        userID: my_user_id
    }
    :return:
    """
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    username = res['username']
    user = MyUser.objects.get(user__username=username)

    user.gender = int(request.GET['gender'])
    user.age = request.GET['age']
    user.address_provinces = request.GET['addressProvinces']
    user.address_city = request.GET['addressCity']
    user.signature = request.GET['signature']
    user.save()
    return JsonResponse({"result": "yes"})


def edit_profile(request):
    """
    更改头像
    :param request: 用户ID, 图片文件
    :return:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    # if request.method == 'GET':
    print(request.FILES)
    image = Image(img=request.FILES.get('file'))
    image.save()
    username = res["username"]
    user = MyUser.objects.get(user__username=username)
    user.profile = image.id
    user.save()
    return JsonResponse(data={"result": "upload success"})

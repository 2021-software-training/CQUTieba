import json

from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from mainpage.models import Article, Comment, LikeList, Image
from login.models import MyUser, NumCounter
from image.models import Image
from mainpage.utils import user_authentication
from image import show_img


def get_userinfo(request):
    """
    获得用户的基本个人信息，
    :param request: {
        username: my_username
    }
    :return
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        my_username = request.GET['username']
        data = {}
        try:
            my_user = MyUser.objects.get(username=my_username)
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
            data["fontSize"] = my_user.font_size
            data["profile"] = show_img(my_user.profile)
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
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        my_old_username = request.GET['oldUsername']
        my_new_username = request.GET['newUsername']
        data = {}
        try:
            # 新用户名已经存在
            my_user = MyUser.objects.get(user__username=my_new_username)
            data = {"result": "no"}
        except MyUser.DoesNotExist:
            # 新用户名不存在
            data["username"] = my_new_username

            new_email = request.GET['email']
            data["email"] = new_email
            new_gender = request.GET['gender']
            data["gender"] = new_gender
            new_age = request.GET['age']
            data["age"] = new_age
            new_address_provinces = request.GET['addressProvinces']
            data["addressProvinces"] = new_address_provinces
            new_address_city = request.GET['addressCity']
            data["addressCity"] = new_address_city

            new_habits1 = request.GET['habits1']
            data["habits1"] = new_habits1
            new_habits2 = request.GET['habits2']
            data["habits2"] = new_habits2
            new_habits3 = request.GET['habits3']
            data["habits3"] = new_habits3
            new_signature = request.GET['signature']
            data["signature"] = new_signature
            new_exp_value = request.GET['expValue']
            data["expValue"] = new_exp_value
            new_font_size = request.GET['fontSize']
            data["fontSize"] = new_font_size

            # 保存新用户信息
            my_user = MyUser(**data)
            my_user.save()
            # 删除旧用户信息
            MyUser.objects.get(user__username=my_old_username).delete()

        return JsonResponse(data=data)


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

    if request.method == 'GET':
        image = Image(img=request.FILES.get('profile'))
        image.save()
        MyUser.objects.get(user_id=request.GET['userID']).update(profile=image.id)
    return JsonResponse(data={"result": "upload success"})

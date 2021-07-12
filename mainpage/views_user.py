import json
from django.http import HttpResponse, JsonResponse
from login.models import MyUser


def get_userinfo(request):
    """
    获得用户的基本个人信息，
    :param request: {
        userID: my_user_id
    }
    :return
    """

    if request.method == "GET":
        my_user_id = request.GET['userID']
        data = {}
        try:
            my_user = MyUser.objects.get(pk=my_user_id)
            data["userID"] = my_user_id
            data["username"] = my_user.user.username
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
    :param request:
    :return:
    """


def edit_avatar(request):
    """
    修改头像
    :param request:
    :return:
    """
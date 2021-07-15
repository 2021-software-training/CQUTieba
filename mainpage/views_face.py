import json

from django.core.files import File
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from mainpage.utils import user_authentication
from face import face_register, face_update, face_search


def register_face(request):
    """
    人脸注册(需登录后再录入人脸信息)
    :param request: {userID, picURL}
    :return: {result: "yes"/"no"}
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        url = str(request.GET['picURL'])
        user_id = request.GET['userID']
        face_register(url, user_id)
        return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')

    return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')


def update_face(request):
    """
    人脸信息更新(需登录后再录入人脸信息)
    :param request: {userID, picURL}
    :return: {result: "yes"/"no"}
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        url = str(request.GET['picURL'])
        user_id = request.GET['userID']
        face_update(url, user_id)
        return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')

    return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')


def face_login(request):
    """
    人脸登录
    :param request: {picURL}
    :return: {result: "yes"/"no"}
    """
    if request.method == "GET":
        result = face_search(request.GET['picURL'])
        if result:
            return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')

    return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')

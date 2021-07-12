import json

from playsound import playsound
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from mainpage.models import Article, Comment, LikeList
from login.models import MyUser, NumCounter
from mainpage.utils import user_authentication
from text_to_audio import create_MP3
from audio_to_text import get_text


def play_article(request):
    """
    调用create_MP3将文章转为MP3音频文件并播放
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    # playsound('xx.mp3')
    pass


def play_comment(request):
    """
    调用create_MP3将评论转为MP3音频文件并播放
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    # playsound('xx.mp3')
    pass


def audio_input(request):
    """
    语音输入wav文件, 调用get_text获得文字
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    pass

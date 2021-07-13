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
    播放文章的MP3音频文件
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    article = Article.object.get(article_id=request.GET['articleID'])
    playsound(article.article_audio)
    return


def play_comment(request):
    """
    播放评论的MP3音频文件
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    comment = Comment.object.get(comment_id=request.GET['commentID'])
    playsound(comment.comment_audio)
    return


def audio_input(request):
    """
    语音输入wav文件, 调用get_text获得文字
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    filepath = request.GET['filepath']
    data = dict()
    data["result"] = get_text(filepath)
    return JsonResponse(data=data)

import json
from django.http import HttpResponse, JsonResponse

from login.models import MyUser
from mainpage.models import Article, Comment, Audio
from mainpage.utils import user_authentication
from mainpage.text_to_audio import create_MP3, create_MP3_comment


def get_audio_info(request):
    """
    获得audio的设置
    :param request:
    :return:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    username = res['username']
    user = MyUser.objects.get(user__username=username)
    audio_data = {
        'speed':    user.audio_speed,
        'pitch':    user.audio_pitch,
        'volume':   user.audio_volume,
        'person':   user.audio_person
    }
    return JsonResponse(audio_data)


def edit_audio(request):
    """
    编辑用户audio设置信息
    :param request:
    :return:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    username = res['username']
    user = MyUser.objects.get(user__username=username)

    user.audio_speed = request.GET['speed']
    user.audio_pitch = request.GET['pitch']
    user.audio_volume = request.GET['volume']
    user.audio_person = request.GET['person']
    user.save()
    return JsonResponse({"result": "yes"})


def get_audio(request, audio_id):
    audio = Audio.objects.get(pk=audio_id)
    audio_path = str(audio.audio)
    audio_data = open(audio_path, 'rb').read()
    return HttpResponse(audio_data, content_type='audio/mp3')


def audio_article(request):
    """
    生成文章音频 MP3文件并储存
    :param request:
    :return:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})
    username = res['username']
    user = MyUser.objects.get(user__username=username)
    article = Article.objects.get(article_id=request.GET["articleID"])
    # 此时还没生成语音，需要生成
    text = article.article_text
    per = user.audio_person  # 0,1,3,4
    spd = user.audio_speed   # 0-15
    pit = user.audio_pitch   # 0-15
    vol = user.audio_volume  # 0-9

    filepath = create_MP3(text, article.article_id, 'audio', per, spd, pit, vol)
    audio = Audio(audio=filepath)
    audio.save()
    article.article_audio = audio.id
    article.save()

    return JsonResponse({"result": "yes", "articleID": article.article_id, "audioID": article.article_audio})


def audio_comment(request):
    """
    生成评论音频 MP3文件并储存
    :param request:
    :return:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    comment = Comment.objects.get(comment_id=request.GET["commentID"])
    text = comment.comment_text
    per = request.GET["PER"]  # 0,1,3,4
    spd = request.GET["SPD"]  # 0-15
    pit = request.GET["PIT"]  # 0-15
    vol = request.GET["VOL"]  # 0-9

    filepath = create_MP3_comment(text, comment.id, 'audio', per, spd, pit, vol)
    audio = Audio(audio=filepath)
    audio.save()
    comment.comment_audio = audio.id
    comment.save()
    return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')

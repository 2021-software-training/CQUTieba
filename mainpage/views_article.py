import json

from django.core.files import File
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from mainpage.models import Article, Comment, LikeList
from login.models import MyUser, NumCounter
from mainpage.utils import user_authentication
from text_to_audio import create_MP3


def add_article(request):
    """
    用于新增文章
    :param request: {
        articleID, authorID, articleText
            articleAudio(默认先不管这个 默认这个为空) articleTitle
                articleType1 articleType2 articleType3
        }
    :return: json形式的 {result: "yes"/"no"}
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        counter = NumCounter.objects.get(pk=1)
        article = Article(
            article_id=counter.my_article_id,
            author_id=request.GET['authorID'],
            article_text=request.GET['articleText'],
            article_audio=None,
            article_title=request.GET['articleTitle'],
            article_type1=request.GET['articleType1'],
            article_type2=request.GET['articleType2'],
            article_type3=request.GET['articleType3'],
        )
        article.save()
        PER = request.GET['PER']  # 人物, 取值0, 1, 3, 4
        SPD = request.GET['SPD']  # 语速, 取值0-15
        PIT = request.GET['PIT']  # 音调, 取值0-15
        VOL = request.GET['VOL']  # 音量, 取值0-9
        filepath = create_MP3(request.GET['articleText'], PER, SPD, PIT, VOL)
        f = open(filepath, 'rb')
        article.article_audio.save(article.article_id + '.mp3', File(f))
        counter.my_article_id += 1

        return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')
    return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')


def show_an_article(request):
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        article_id = int(request.GET["articleID"])
        try:
            article = Article.objects.get(pk=article_id)
            author_id = article.author_id
            user = MyUser.objects.get(my_user_id=author_id)

            # 判断是否已经有点赞了
            temp = LikeList.objects.filter(article_id=article_id, author_id=author_id)
            likes_judge = bool(temp)

            comments = Comment.objects.filter(article_id=article_id)

            data = {
                "userName": user.user.username,
                "authorID": user.my_user_id,
                "articleID": article.article_id,
                "articleText": article.article_text,
                "articleViews": article.article_views,
                "articleTime": str(article.article_time),
                # "articleAudio": article_audio,
                "articleTitle": article.article_title,
                "likesNum": article.likes_num,
                "commentsNum": article.comments_num,
                "articleType1": article.article_type1,
                "articleType2": article.article_type2,
                "article_type3": article.article_type3,
                "likeJudge": likes_judge
            }
            article.article_views += 1
            article.save()
            return HttpResponse(json.dumps({"result": data}), 'application/json')
        except Article.DoesNotExist:
            return HttpResponse(json.dumps({"result": "does not exist"}), 'application/json')
    else:
        return HttpResponse(json.dumps({"result": "not GET"}), 'application/json')


def show_all_articles(request):
    """
    展示所有文章
    :param request {
        type:
    }:
    :return:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    articles_type = request.GET["type"]
    if articles_type != "all":
        articles_temp = Article.objects.filter(
            Q(article_type1=articles_type) | Q(article_type2=articles_type) | Q(article_type3=articles_type)
        )
        articles = articles_temp.order_by('-article_time', '-likes_num', '-comments_num', '-article_views')
    else:
        articles = Article.objects.all().order_by('-article_time', '-likes_num', '-comments_num', '-article_views')

    articles_data = []
    for x in articles:
        temp = dict()
        temp['title'] = x.article_title
        temp['time'] = ("{:}年{:}月{:}日".format(str(x.article_time.year), str(x.article_time.month), str(x.article_time.day)))
        temp['articleType1'] = x.article_type1
        temp['articleType2'] = x.article_type2
        temp['articleType3'] = x.article_type3
        temp['articleID'] = x.article_id
        articles_data.append(temp)
    return JsonResponse(data=articles_data, safe=False)


def show_user_article(request):
    """
    获得指定用户的历史文章，并将文章放入列表之中[article1, article2, ....]
    article为dict <--> json
    包括文章ID, 标题title, 时间time, 点赞数likes_num, 类别1article_type1, 类别2article_type2, 类别3article_type3
    :param request {
        authorID: author_id
        }:
    :return [article1, article2, ....]:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    articles = Article.objects.filter(author_id=request.GET['authorID']) \
        .order_by('-article_time')
    articles_data = []
    for x in articles:
        temp = dict()
        temp['ID'] = x.article_id
        temp['title'] = x.article_title
        temp['time'] = str(x.article_time)
        temp['likesNum'] = x.likes_num
        temp['commentsNum'] = x.comments_num
        temp['articleType1'] = x.article_type1
        temp['articleType2'] = x.article_type2
        temp['articleType3'] = x.article_type3
        articles_data.append(temp)
    return JsonResponse(data=articles_data, safe=False)

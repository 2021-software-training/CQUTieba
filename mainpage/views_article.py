from django.http import HttpResponse, JsonResponse
from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet
from mainpage.utils import user_authentication, get_user_name
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json


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
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        counter = NumCounter.objects.get(pk=1)
        article = Article(
            article_id=counter.my_article_id,
            author_id=request.GET['authorID'],
            article_text=request.GET['articleText'],
            article_audio="",
            article_title=request.GET['articleTitle'],
            article_type1=request.GET['articleType1'],
            article_type2=request.GET['articleType2'],
            article_type3=request.GET['articleType3'],
        )
        counter.my_article_id += 1
        article.save()
        return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')
    return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')


def edit_article(request):
    """

    :param request:
    :return:
    """
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    article_id = request.GET["articleID"]

    article = Article(
        author_id=request.GET['authorID'],
        article_text=request.GET['articleText'],
        article_audio="",
        article_title=request.GET['articleTitle'],
        article_type1=request.GET['articleType1'],
        article_type2=request.GET['articleType2'],
        article_type3=request.GET['articleType3'],
    )

    return JsonResponse(data={'result': "success"})


def show_an_article(request):
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        article_id = int(request.GET["articleID"])
        try:
            article = get_object_or_404(Article, pk=article_id)
            author_id = article.author_id
            user = MyUser.objects.get(my_user_id=author_id)

            # 判断是否已经有点赞了
            temp = LikeList.objects.filter(article_id=article_id, user_id=author_id)
            likes_judge = bool(temp)

            comments = Comment.objects.filter(article_id=article_id)

            data = {
                "authorName": user.user.username,
                "authorID": user.my_user_id,
                "articleID": article.article_id,
                "articleText": article.article_text,
                "articleTime": str(article.article_time),
                # "articleAudio": article_audio,
                "articleTitle": article.article_title,
                "likesNum": article.likes_num,
                "commentsNum": article.comments_num,
                "articleType1": article.article_type1,
                "articleType2": article.article_type2,
                "articleType3": article.article_type3,
                "likeJudge": likes_judge
            }
            article.article_views += 1
            article.save()
            return JsonResponse(data=data)
        except Article.DoesNotExist:
            return JsonResponse({"result": "does not exist"})
    else:
        return JsonResponse({"result": "not GET"})


def show_page_all_articles(request):
    """
    展示所有文章
    :param request {
        type:
    }:
    :return:
    """
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    articles_type = request.GET["type"]
    if articles_type != "All":
        articles_temp = Article.objects.filter(
            Q(article_type1=articles_type) | Q(article_type2=articles_type) | Q(article_type3=articles_type)
        )
        articles = articles_temp.order_by('-article_time', '-likes_num', '-comments_num', '-article_views')
    else:
        articles = Article.objects.all().order_by('-article_time', '-likes_num', '-comments_num', '-article_views')

    articles_data = []
    for x in articles:
        temp = dict()
        temp['articleID'] = x.article_id
        temp['title'] = x.article_title
        temp['time'] = ("{:}年{:}月{:}日".format(
                str(x.article_time.year),
                str(x.article_time.month),
                str(x.article_time.day)
            ))
        temp['authorName'] = get_user_name(x)
        temp['articleType1'] = x.article_type1
        temp['articleType2'] = x.article_type2
        temp['articleType3'] = x.article_type3
        temp['articleText'] = x.article_text
        temp['articleID'] = x.article_id
        temp['commentsNum'] = x.comments_num
        temp['likesNum'] = x.likes_num
        articles_data.append(temp)
    return JsonResponse(data=articles_data, safe=False)


def show_user_all_articles(request):
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
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    username = res["username"]
    user = MyUser.objects.get(user__username=username)

    articles = Article.objects.filter(author_id=user.my_user_id).order_by('-article_time')
    articles_data = []
    for x in articles:
        temp = dict()
        temp['articleID'] = x.article_id
        temp['title'] = x.article_title
        temp['time'] = ("{:}年{:}月{:}日".format(
                str(x.article_time.year),
                str(x.article_time.month),
                str(x.article_time.day)
            ))
        temp['articleType1'] = x.article_type1
        temp['articleType2'] = x.article_type2
        temp['articleType3'] = x.article_type3
        temp['articleText'] = x.article_text
        temp['articleID'] = x.article_id
        temp['viewsNum'] = x.article_views
        temp['commentsNum'] = x.comments_num
        temp['likesNum'] = x.likes_num
        articles_data.append(temp)
    return JsonResponse(data=articles_data, safe=False)

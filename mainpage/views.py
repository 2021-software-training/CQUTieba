import json
from django.http import HttpResponse, JsonResponse
from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet


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


def add_comment(request):
    """
    :param request: {
        commentText, commentID, articleID
            commentAudio(先默认为空)
        }
    :return:
    """


def add_like(request):
    """
    添加点赞
    对指定文章添加点赞数，并操控LikeList表，添加一对 文章 <-> 用户 点赞关联
    :param request: {
        articleID, userID
        }
    :return void:
    """
    if request.method == "GET":
        like_article_id = request.GET['articleID']
        like_user_id = request.GET['userID']
        try:
            # 该用户点赞过该文章, 撤销点赞, 删除点赞关联
            LikeList.objects.get(article_id=like_article_id, user_id=like_user_id).delete()
            new_like_num = Article.objects.get(article_id=like_article_id).likes_num - 1
            Article.objects.get(article_id=like_article_id).update(likes_num=new_like_num)
        except LikeList.DoesNotExist:
            # 该用户未点赞该文章, 进行点赞, 增加点赞关联
            new_like = LikeList(
                article_id=like_article_id,
                user_id=like_user_id,
            )
            new_like.save()
            new_like_num = Article.objects.get(article_id=like_article_id).likes_num + 1
            Article.objects.get(article_id=like_article_id).update(likes_num=new_like_num)
    return


def show_an_article(request):
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
        page_num:
    }:
    :return:
    """
    articles = Article.objects.all().order_by('-article_time', '-likes_num', '-comments_num', '-article_views')
    articles_data = []
    for x in articles:
        temp = dict()
        temp['ID'] = x.article_id
        temp['title'] = x.article_title
        temp['time'] = str(x.article_time)
        temp['likes_num'] = x.likes_num
        temp['articleType1'] = x.article_type1
        temp['articleType2'] = x.article_type2
        temp['articleType3'] = x.article_type3
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
    articles = Article.objects.get(author_id=request.GET['authorID']) \
        .order_by('-article_time', '-likes_num', '-comments_num', '-article_views')
    articles_data = []
    for x in articles:
        temp = dict()
        temp['ID'] = x.article_id
        temp['title'] = x.article_title
        temp['time'] = str(x.article_time)
        temp['likes_num'] = x.likes_num
        temp['articleType1'] = x.article_type1
        temp['articleType2'] = x.article_type2
        temp['articleType3'] = x.article_type3
        articles_data.append(temp)
    return JsonResponse(data=articles_data, safe=False)

import json
from django.http import HttpResponse
from mainpage.models import Article, LikeList
from login.models import MyUser


def add_article(request):
    """
    用于新增文章
    :param request: {
        articleID, authorId, articleText
            articleAudio(默认先不管这个 默认这个为空) articleTitle
                articleType1 articleType2 articleType3
        }
    :return: json形式的 {result: "yes"/"no"}
    """
    pass


def add_comment(request):
    """

    :param request: {
        commentText, commentID, articleID
            commentAudio(先默认为空)
        }
    :return:
    """


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
    pass

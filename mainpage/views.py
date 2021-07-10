import json
from django.http import HttpResponse
from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter


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
    if request.method == "GET":
        add_authorID = request.GET['authorID']
        add_articleText = request.GET['articleText']
        add_articleAudio = ""
        add_articleTitle = request.GET['articleTitle']
        add_articleType1 = request.GET['articleType1']
        add_articleType2 = request.GET['articleType2']
        add_articleType3 = request.GET['articleType3']
        counter = NumCounter.objects.get(pk=1)
        article = Article(
            article_id=counter.my_article_id,
            author_id=add_authorID,
            article_text=add_articleText,
            article_audio=add_articleAudio,
            article_title=add_articleTitle,
            article_type1=add_articleType1,
            article_type2=add_articleType2,
            article_type3=add_articleType3,
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
        like_articleID = request.GET['articleID']
        like_userID = request.GET['userID']
        try:
            # 该用户点赞过该文章, 撤销点赞
            LikeList.objects.get(article_id=like_articleID, user_id=like_userID).delete()
            new_like_num = Article.objects.get(article_id=like_articleID).likes_num - 1
            Article.objects.get(article_id=like_articleID).update(likes_num=new_like_num)
        except LikeList.DoesNotExist:
            # 该用户未点赞该文章, 进行点赞
            new_like = LikeList(
                article_id=like_articleID,
                user_id=like_userID,
            )
            new_like.save()
            new_like_num = Article.objects.get(article_id=like_articleID).likes_num + 1
            Article.objects.get(article_id=like_articleID).update(likes_num=new_like_num)
    return

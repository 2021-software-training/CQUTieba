import json

from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from mainpage.models import Article, Comment, LikeList, LikeListComment
from login.models import MyUser, NumCounter
from mainpage.utils import user_authentication


def add_article_like(request):
    """
    对指定文章添加点赞数，并操控LikeList表，添加一对 文章 <-> 用户 点赞关联
    :param request: {
        articleID, userID
        }
    :return:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

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

    return JsonResponse(data={"result": 1})


def add_comment_like(request):
    """
    对指定评论添加点赞数，并操控LikeList表，添加一对 评论 <-> 用户 点赞关联
    :param request: {
        commentID, userID
        }
    :return void:
    """
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        like_comment_id = request.GET['commentID']
        like_user_id = request.GET['userID']
        try:
            # 该用户点赞过该评论, 撤销点赞, 删除点赞关联
            LikeListComment.objects.get(comment_id=like_comment_id, user_id=like_user_id).delete()
            new_like_num = Comment.objects.get(comment_id=like_comment_id).likes_num - 1
            Comment.objects.get(comment_id=like_comment_id).update(likes_num=new_like_num)
        except LikeList.DoesNotExist:
            # 该用户未点赞该评论, 进行点赞, 增加点赞关联
            new_like = LikeListComment(
                comment_id=like_comment_id,
                user_id=like_user_id,
            )
            new_like.save()
            new_like_num = Comment.objects.get(comment_id=like_comment_id).likes_num + 1
            Comment.objects.get(comment_id=like_comment_id).update(likes_num=new_like_num)

    return JsonResponse(data={"result": 1})

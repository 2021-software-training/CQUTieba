import json
from django.http import HttpResponse, JsonResponse
from mainpage.models import Article, Comment, LikeList, LikeListComment, Image, Audio
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet
from mainpage.utils import user_authentication
from mainpage.text_to_audio import create_MP3


def add_like_article(request):
    """
    添加点赞
    对指定文章添加点赞数，并操控LikeList表，添加一对 文章 <-> 用户 点赞关联
    :param request: {
        articleID
        }
    :return void:
    """
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    if request.method == "GET":
        username = res["username"]
        user = MyUser.objects.get(user__username=username)
        like_article_id = request.GET['articleID']
        like_user_id = user.my_user_id
        try:
            # 该用户点赞过该文章, 撤销点赞, 删除点赞关联
            LikeList.objects.get(article_id=like_article_id, user_id=like_user_id).delete()
            article = Article.objects.get(article_id=like_article_id)
            article.likes_num -= 1
            article.save()
            return JsonResponse({"result": "yes"})
        except LikeList.DoesNotExist:
            # 该用户未点赞该文章, 进行点赞, 增加点赞关联
            new_like = LikeList(
                article_id=like_article_id,
                user_id=like_user_id,
            )
            new_like.save()
            article = Article.objects.get(article_id=like_article_id)
            article.likes_num += 1
            article.save()
            return JsonResponse({"result": "yes"})


def add_like_comment(request):
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
        username = res["username"]
        user = MyUser.objects.get(user__username=username)
        like_user_id = user.my_user_id
        try:
            # 该用户点赞过该评论, 撤销点赞, 删除点赞关联
            LikeListComment.objects.get(comment_id=like_comment_id, user_id=like_user_id).delete()
            comment = Comment.objects.get(comment_id=like_comment_id)
            comment.likes_num -= 1
            comment.save()
            return JsonResponse({"result": "yes"})

        except LikeList.DoesNotExist:
            # 该用户未点赞该评论, 进行点赞, 增加点赞关联
            new_like = LikeListComment(
                comment_id=like_comment_id,
                user_id=like_user_id,
            )
            new_like.save()
            comment = Comment.objects.get(comment_id=like_comment_id)
            comment.likes_num += 1
            comment.save()

    return JsonResponse(data={"result": 1})


def get_image(request, username):
    user = MyUser.objects.get(user__username=username)
    img_id = user.profile

    img = Image.objects.get(pk=img_id)
    image_path = str(img.img)
    img_data = open(image_path, 'rb').read()
    return HttpResponse(img_data, content_type='image/jpg')


def delete_comment(request):
    res = user_authentication(request)
    print(res)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    comment = Comment.objects.get(comment_id=request.GET["commentID"])
    comment.delete()
    return JsonResponse({"result": "yes"})

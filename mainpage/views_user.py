import json
from django.http import HttpResponse, JsonResponse
from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet


def get_userinfo(request):
    """
    获得用户的基本个人信息，
    :param request: {
        userID: my_user_id
    }
    :return
    """


def show_user_comment(request):
    """
    获得指定用户的历史评论，并将评论放入列表之中[article1, article2, ....]
    article为dict <--> json
    包括被评论文章的id, 标题title，时间time，类别1article_type1, 类别2article_type2，类别3article_type3
    评论时间time, 评论的内容
    :param request:

    message {
        comment {

        },
        article {

        }
    }
    :return: [message1, message2, .....]
    """

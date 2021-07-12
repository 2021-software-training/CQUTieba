import json
from django.http import HttpResponse, JsonResponse
from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet


def add_comment(request):
    """

    :param request: {
        commentText, commentID, articleID
            commentAudio(先默认为空)
        }
    :return:
    """


def show_user_comment(request):
    """
    获得指定用户的历史评论，并将评论放入列表之中[article1, article2, ....]（时间顺序）
    article为dict <--> json
    包括被评论文章的id, 评论的id，标题title，时间time，类别1article_type1, 类别2article_type2，类别3article_type3
    评论时间time, 评论的内容
    :param request:

    message {
        comment {
            commentID.....
            commentText....
        },
        article {
            title....
            time.....
        }
    }
    :return: [message1, message2, .....]
    """


def edit_comment(request):
    """
    用于修改或者删除用户的历史评论
    :param request: {
        commentID       :   comment_id,
        newCommentText  :   comment_text,
        isDelete        :   is_delete   ("1"为删除该评论，"0"为修改该评论)
    }
    :return:
    """
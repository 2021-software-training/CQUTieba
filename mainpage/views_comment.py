import json
from django.http import HttpResponse, JsonResponse
from mainpage.models import Article, Comment, LikeList
from login.models import NumCounter, MyUser
from django.db.models.query import QuerySet
from mainpage.utils import user_authentication


# 需要修改一下
def add_comment(request):
    """
       :param request: {
           commentText, commentID, articleID
               commentAudio(先默认为空)
           }
       :return:
       """
    if request.method == "GET":
        comment_text = request.GET(['comment_text'])
        commenter_id = request.GET(['commenter_id'])
        article_id = request.GET(['article_id'])
        # 查询这篇文章的作者在不在
        comment_target = Article.objects.filter(article_id=article_id)

        # 返回值是不是True
        if comment_target:
            # 查询id
            comment_target_name = comment_target[0].author_id
            comment_text += "\n"+"{0} 评论 {1}".format(commenter_id, comment_target_name)
            comment_this = Comment(
                comment_text=comment_text,
                commenter_id=commenter_id,
                article_id=article_id,
            )
            comment_this.save()
            return HttpResponse(json.dumps({"result": "yes", "commenter": commenter_id}))
        else:
            # 回复的
            comment_target = Comment.objects.filter(article_id=article_id)
            # 查询id
            comment_target_name = comment_target[0].article_id
            comment_text += "\n"+"{0} 回复 {1}".format(commenter_id, comment_target_name)
            comment_this = Comment(
                comment_text, commenter_id, article_id,
            )
            comment_this.save()  # 加入到数据库当中去

            return JsonResponse({"result": "yes", "commenter": commenter_id})
    return JsonResponse({"result": "no"})


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
    res = user_authentication(request)
    if not res["result"]:
        return JsonResponse(data={"result": 0})

    comments = Comment.objects.filter(commenter_id=request.GET['commenterID']).order_by('-comment_time')
    comments_data = []
    for x in comments:
        temp_c = dict()
        temp_c['commentText'] = x.comment_text
        temp_c['commentID'] = x.comment_id
        temp_c['commentLikesNum'] = x.likes_num
        temp_c['commentAudio'] = x.comment_audio
        temp_c['commentTime'] = x.comment_time
        a = Article.objects.get(article_id=x.article_id)
        temp_a = dict()
        temp_a['articleID'] = a.article_id
        temp_a['articleTime'] = a.article_time
        temp_a['articleTitle'] = a.article_title
        temp_a['articleType1'] = a.article_type1
        temp_a['articleType2'] = a.article_type2
        temp_a['articleType3'] = a.article_type3
        temp = dict()
        temp['comment'] = temp_c
        temp['article'] = temp_a
        comments_data.append(temp)

    return JsonResponse(data=comments_data, safe=False)


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
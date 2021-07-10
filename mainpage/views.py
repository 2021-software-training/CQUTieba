from django.shortcuts import render
from mainpage.models import *
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
'''
    
'''

def add_comment(request):#第一次加入文章
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
        comment_target = Article.objects.get(article_id=article_id)#查询这篇文章的作者在不在
        if(comment_target[1]):#返回值是不是True
            comment_target_name = comment_target.author_id#查询id
            comment_text += "\n"+"{0} 评论 {1}".format(commenter_id,comment_target_name)
            comment_this = Comment(
                comment_text,commenter_id,article_id,
                comment_audio
            )
            comment_this.save()#加入到数据库当中去
            return HttpResponse(json.dumps({"result": "yes","commenter":commenter_id}))
        else:
            comment_target = Comment.objects.get(comment_id=article_id)#回复的
            comment_text+="\n"+"{0} 回复 {1}".format(commenter_id,comment_target_name)
            comment_this=Comment(
                comment_text,commenter_id,article_id,
                comment_audio
            )
            comment_this.save()  #加入到数据库当中去
            return HttpResponse(json.dumps({"result":"yes","commenter":commenter_id}))
    return HttpResponse(json.dumps({"result":"no"}))






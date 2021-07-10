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
        comment_text += "\n"+"{0} 回复 {1}".format(commenter_id,article_id)
        comment_this = Comment(
            comment_text,commenter_id,article_id,
            comment_audio
        )
        comment_this.save()#加入到数据库当中去
        return HttpResponse(json.dumps({"result": "yes","commenter":commenter_id}))
    return HttpResponse(json.dumps({"result":"no"}))






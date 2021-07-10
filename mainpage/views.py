from django.shortcuts import render
from mainpage.models import *
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
'''
    
'''

def add_comment(request):#第一次加入文章
    if(request.method=="GET"):
        comment_text=request.GET(['comment_text'])
        commenter_id=request.GET(['commenter_id'])
        article_id=request.GET(['article_id'])
        likes_num=0
        comment_audio=request.GET(['comment_audio'])
        comment_time=request.GET(['comment_time'])
        comment_text+="\n"+"{0} 回复 {1}".format(commenter_id,article_id)
        comment_this=Comment(
            comment_text,commenter_id,article_id,
            likes_num,comment_audio,comment_time
        )
        comment_this.save()#加入到数据库当中去
        return HttpResponse(json.dumps({"result": "yes","commenter":commenter_id,"comment_target":article_id}))
    return HttpResponse(json.dumps({"result":"no"}))






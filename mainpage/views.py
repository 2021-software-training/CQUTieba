from django.shortcuts import render
from mainpage.models import *
from django.http import HttpResponse,HttpResponseRedirect
from audio import *
from django.core.files import File
from mainpage.utils import audioInfo#引入
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
# Create your views here.
'''
    
'''
def get_audio(request,text,user_id):#生成文件
    """
        用于完成判定后要增加语音的功能
        :param PER: 发音人, 0为度小美，1为度小宇，3为度逍遥，4为度丫丫
        :param SPD: 语速，取值0-15，默认为5中语速
        :param PIT: 音调，取值0-15，默认为5中语调
        :param VOL: 音量，取值0-9，默认为5中音量
    """
    if request.method == 'GET':
        PER = request.GET(['PER'])
        SPD = request.GET(['SPD'])
        PIT = request.GET(['PIT'])
        VOL = request.GET(['VOL'])
        audio_this = audioInfo(PER = PER,
                               SPD = SPD,
                               PIT = PIT,
                               VOL = VOL)
        audio_this.add_audio(text,user_id)
        return HttpResponse(request,"声纹信息录入完毕")
    return HttpResponse("声纹信息异常")
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
        add_chose_audio = request.GET['article_chose_audio']#是否要上传声纹信息
        add_articleTitle = request.GET['articleTitle']
        add_articleType1 = request.GET['articleType1']
        add_articleType2 = request.GET['articleType2']
        add_articleType3 = request.GET['articleType3']
        counter = NumCounter.objects.get(pk=1)
        article=Article(
            article_id=counter.my_article_id,
            author_id=add_authorID,
            article_text=add_articleText,
            article_audio=add_articleAudio,
            article_chose_audio=add_chose_audio,#是否需要加入语音信息
            article_title=add_articleTitle,
            article_type1=add_articleType1,
            article_type2=add_articleType2,
            article_type3=add_articleType3,
        )
        if add_chose_audio:
            get_audio(add_articleText,add_authorID)
            f=open('Result{0}.mp3'.format(add_authorID),'rb')
            article.article_audio.save('Reuslt{0}.mp3'.format(add_authorID),File(f))
            f.close()
        counter.my_article_id += 1
        article.save()
        if add_chose_audio:#完成后删除文件
            os.remove('Result{0}.mp3'.format(add_authorID))
            f_list=os.listdir(os.getcwd())
            for i in f_list:
                # os.path.splitext():分离文件名与扩展名
                if os.path.splitext(i)[1]=='.mp3':
                    os.remove(i)#删除文件
        return HttpResponse(json.dumps({"result": "yes"}), content_type='application/json')
    return HttpResponse(json.dumps({"result": "no"}), content_type='application/json')

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
        comment_target = Article.objects.filter(article_id=article_id)#查询这篇文章的作者在不在
        if(comment_target):#返回值是不是True
            comment_target_name = comment_target[0].author_id#查询id
            comment_text += "\n"+"{0} 评论 {1}".format(commenter_id,comment_target_name)

            comment_this = Comment(
                comment_text,commenter_id,article_id,
                comment_audio
            )
            comment_this.save()#加入到数据库当中去
            return HttpResponse(json.dumps({"result": "yes","commenter":commenter_id}))
        else:
            comment_target = Comment.objects.filter(article_id=article_id)#回复的
            comment_target_name=comment_target[0].article_id  #查询id
            comment_text+="\n"+"{0} 回复 {1}".format(commenter_id,comment_target_name)
            comment_this=Comment(
                comment_text,commenter_id,article_id,
                comment_audio
            )
            comment_this.save()  #加入到数据库当中去
            return HttpResponse(json.dumps({"result":"yes","commenter":commenter_id}))
    return HttpResponse(json.dumps({"result":"no"}))
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
    #按照评论者的id
    if request.method=='GET':
        commentID = request.GET(['comment_id'])
        isDelete=request.GET(['is_delete'])
        if isDelete:
            target_comment = Comment.objects.filter(comment_id = commentID)
            if(target_comment):
                target_comment.delete()
            else:
                return HttpResponse("评论不存在")
        else:
            newCommentText = request.GET(['comment_text'])
            target_comment = Comment.objects.filter(comment_id = commentID)
            if target_comment:
                target_comment[0].comment_txet = newCommentText
                target_comment[0].save()
            else:
                return HttpResponse("评论不存在")
        return HttpResponse("操作成功")


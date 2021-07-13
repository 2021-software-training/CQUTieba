from django.test import TestCase
import sys
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CQUTieba.settings')
django.setup()
# Create your tests here.
#def create_MP3(TEXT, PER=0, SPD=5, PIT=5, VOL=5):
from mainpage.models import Article,Comment
from mainpage.utils import audioInfo
from django.core.files import File
from mainpage.audio import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse,JsonResponse
def get_audio(text,user_id):#生成文件
    """
        用于完成判定后要增加语音的功能
        :param PER: 发音人, 0为度小美，1为度小宇，3为度逍遥，4为度丫丫
        :param SPD: 语速，取值0-15，默认为5中语速
        :param PIT: 音调，取值0-15，默认为5中语调
        :param VOL: 音量，取值0-9，默认为5中音量
    """
    PER = 3
    SPD = 5
    PIT = 5
    VOL = 5
    audio_this = audioInfo(PER = PER,
                           SPD = SPD,
                           PIT = PIT,
                           VOL = VOL)
    audio_this.add_audio(text,user_id)
def add_article(add_authorID,
                add_articleText,
                add_articleAudio,
                add_chose_audio,
                add_articleTitle,
                add_articleType1,
                add_articleType2,
                add_articleType3,):
    """
    用于新增文章
    :param request: {
        articleID, authorId, articleText
            articleAudio(默认先不管这个 默认这个为空) articleTitle
                articleType1 articleType2 articleType3
        }
    :return: json形式的 {result: "yes"/"no"}
    """
    add_authorID = add_authorID
    add_articleText = add_articleText
    add_articleAudio = ""
    add_chose_audio = add_chose_audio#是否要上传声纹信息
    add_articleTitle = add_articleTitle
    add_articleType1 = add_articleType1
    add_articleType2 = add_articleType2
    add_articleType3 = add_articleType3
    #counter = NumCounter.objects.get(pk=1)
    article=Article(
        article_id="13",
        author_id=add_authorID,
        article_text=add_articleText,
        article_audio=add_articleAudio,
        article_chose_audio=add_chose_audio,
        article_title=add_articleTitle,
        article_type1=add_articleType1,
        article_type2=add_articleType2,
        article_type3=add_articleType3,
    )
    if add_chose_audio:
        get_audio(add_articleText,add_authorID)#生成文件并上传
        with open('Result{0}.mp3'.format(add_authorID),'rb') as f:
            article.article_audio.save('Reuslt{0}.mp3'.format(add_authorID),File(f))
            f.close()
    #counter.my_article_id += 1
    article.save()
    #article.objects.all().delete()
    os.remove('Result{0}.mp3'.format(add_authorID))
    f_list=os.listdir(os.getcwd())
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1]=='.mp3':
            os.remove(i)
    #上传之后立刻移除
def add_comment_article(#专门针对评论文章的功能
        comment_id,
        comment_text,
        commenter_id,
        article_id,#目标文章
        is_add_audio#是否要加入语音
):#第一次加入文章
    """
       :param request: {
           commentText, commentID, articleID
               commentAudio(先默认为空)
           }
       :return:
       """
    comment_id = comment_id
    comment_text = comment_text
    commenter_id = commenter_id
    article_id = article_id
    comment_audio=""
    is_add_audio = True
    comment_target = Article.objects.filter(article_id=article_id)#查询这篇文章的作者在不在
    if is_add_audio:
        get_audio(comment_text,commenter_id)#生成对应的文件
        #f=open('Result{0}.mp3'.format(commenter_id),'rb')
        #Comment.article_audio.save('Reuslt{0}.mp3'.format(commenter_id),File(f))
        #f.close()
    if(comment_target):#返回值是是True
        comment_target_name = comment_target[0].author_id#查询id
        comment_this = Comment(
            comment_id,
            comment_text,commenter_id,article_id,0,
            comment_audio
        )
        f=open('Result{0}.mp3'.format(commenter_id),'rb')
        comment_this.comment_audio.save('Reuslt{0}.mp3'.format(commenter_id),File(f))
        f.close()
        if is_add_audio:  #完成后删除文件
            f_list=os.listdir(os.getcwd())
            for i in f_list:
                # os.path.splitext():分离文件名与扩展名
                if os.path.splitext(i)[1]=='.mp3':
                    os.remove(i)  #删除文件
        comment_this.comment_text+="\n"+"{0} 评论 {1}".format(commenter_id,comment_target_name)
        comment_this.save()#加入到数据库当中去
        return True
    else:
        return True
        '''comment_target = Comment.objects.filter(article_id=article_id)#回复的
        comment_target_name=comment_target[0].article_id  #查询id
        comment_this=Comment(
            comment_text,commenter_id,article_id,
            comment_audio
        )
        f=open('Result{0}.mp3'.format(commenter_id),'rb')
        comment_this.comment_audio.save('Reuslt{0}.mp3'.format(commenter_id),File(f))
        f.close()
        if add_chose_audio:  #完成后删除文件
            os.remove('Result{0}.mp3'.format(add_authorID))
            f_list=os.listdir(os.getcwd())
            for i in f_list:
                # os.path.splitext():分离文件名与扩展名
                if os.path.splitext(i)[1]=='.mp3':
                    os.remove(i)  #删除文件
        comment_this.comment_text+="\n"+"{0} 回复 {1}".format(commenter_id,comment_target_name)
        comment_this.save()  #加入到数据库当中去
        return True'''
def add_comment_comment(commentText,commentID,articleID,isAddAudio,commenterID):#针对评论
    """
           :param request: {
               commentText, commentID, articleID
                   commentAudio(先默认为空)
                   commenterID(评论是谁)
               }
           :return:
    """
    commentText = commentText#评论什么
    commentID = commentID#评论
    articleID = articleID#评论的是哪个评论
    isAddAudio = isAddAudio
    commentAudio=""
    commenterID = commenterID
    comment_target=Comment.objects.filter(comment_id=articleID)  #查询这篇文章的作者在不在
    if (comment_target):  #返回值是是True
        comment_target_name=comment_target[0].commenter_id  #查询id
        comment_this=Comment(
            comment_id = commentID,
            comment_text = commentText,
            commenter_id = commenterID,
            article_id = articleID,
            comment_audio = commentAudio,
            comment_to = 0
        )
        if isAddAudio:
            get_audio(commentText,commenterID)  #生成对应的文件
        f=open('Result{0}.mp3'.format(commenterID),'rb')
        comment_this.comment_audio.save('Reuslt{0}.mp3'.format(commenterID),File(f))
        f.close()
        if isAddAudio:  #完成后删除文件
            f_list=os.listdir(os.getcwd())
            for i in f_list:
                # os.path.splitext():分离文件名与扩展名
                if os.path.splitext(i)[1]=='.mp3':
                    os.remove(i)  #删除文件
        comment_this.comment_text+="\n"+"{0} 回复 {1}".format(commenterID,comment_target_name)
        comment_this.save()  #加入到数据库当中去
        return True
    else:
        return False
    return False
def edit_comment(commentID,newCommentText,isDelete):
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
    comment_id = commentID
    is_delete = isDelete
    if is_delete:
        target_comment = Comment.objects.filter(comment_id = commentID)
        if(target_comment):
            target_comment[0].delete()
            return True
        else:
            return True
    else:
        comment_text = newCommentText#新评论
        target_comment = Comment.objects.filter(comment_id = commentID)
        #旧评论
        if target_comment:
            comment_this = target_comment[0]
            if comment_this.comment_to:
                tar = comment_this.comment_text.split('\n')[-1]#最后文本标记信息
                comment_this.comment_text = comment_text
                get_audio(comment_text,comment_this.commenter_id)
                f=open('Result{0}.mp3'.format(comment_this.commenter_id),'rb')
                comment_this.comment_audio.save('Reuslt{0}.mp3'.format(comment_this.commenter_id),File(f))
                f.close()
                f_list=os.listdir(os.getcwd())
                for i in f_list:
                    # os.path.splitext():分离文件名与扩展名
                    if os.path.splitext(i)[1]=='.mp3':
                        os.remove(i)  #删除文件
                comment_this.comment_text += ('\n'+tar)
                comment_this.save()
            else:
                tar=comment_this.comment_text.split('\n')[-1]  #最后文本标记信息
                comment_this.comment_text=comment_text
                get_audio(comment_text,comment_this.commenter_id)
                f=open('Result{0}.mp3'.format(comment_this.commenter_id),'rb')
                comment_this.comment_audio.save('Reuslt{0}.mp3'.format(comment_this.commenter_id),File(f))
                f.close()
                f_list=os.listdir(os.getcwd())
                for i in f_list:
                    # os.path.splitext():分离文件名与扩展名
                    if os.path.splitext(i)[1]=='.mp3':
                        os.remove(i)  #删除文件
                comment_this.comment_text += ('\n'+tar)
                comment_this.save()
            return True
        else:
            return True
    return JsonResponse({"result":"no"})
if __name__=='__main__':
     '''add_comment_article(comment_id=1,
                         comment_text="写的很好",
                         commenter_id=12,
                         article_id=13,
                         is_add_audio=1)'''
     add_comment_comment("这样真好",5,1,1,15)
     #commentText,commentID,articleID,isAddAudio,commenterID
     #edit_comment(5,"我喜欢太空，你呢",0)
     '''add_article(add_authorID=1628,add_articleText="你好世界",
                 add_chose_audio=1,add_articleTitle="wryyyy",
                add_articleAudio="",add_articleType1="1",
                add_articleType2="2",add_articleType3="3")'''
'''
    def add_article(add_authorID,
                    add_articleText,
                    add_articleAudio,
                    add_chose_audio,
                    add_articleTitle,
                    add_articleType1,
                    add_articleType2,
                    add_articleType3,)
                    '''


import sys
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CQUTieba.settings')
django.setup()
from django.test import TestCase
from mainpage.models import  *
from datetime import datetime
# 这两行很重要，用来寻找项目根目录，os.path.dirname要写多少个根据要运行的python文件到根目录的层数决定
import django.utils.timezone as timezone
a = Article(article_id=1,
            author_id=1,
            article_text="wryyy",
            article_views=0,
            article_title="helloworld",
            article_time=timezone.now())
b = Comment(comment_text="no",commenter_id=1,article_id=13,likes_num=0)
c = Comment()
# Create your tests here.
def add_comment(comment_text,commenter_id,article_id):#第一次加入文章
    """
       :param request: {
           commentText, commentID, articleID
               commentAudio(先默认为空)
           }
       :return:
       """
    comment_target = Article.objects.filter(article_id=article_id)#查询这篇文章的作者在不在
    if(comment_target):#返回值是不是True
        comment_target_name = comment_target[0].author_id#查询id
        comment_text += "\n"+"{0} 评论 {1}".format(commenter_id,comment_target_name)
        print(comment_text)
    else:
        comment_target = Comment.objects.filter(article_id=article_id)#回复的
        comment_target_name=comment_target[0].article_id  #查询id
        comment_text+="\n"+"{0} 回复 {1}".format(commenter_id,comment_target_name)
        print(comment_text)

if __name__=='__main__':
    '''Comment.objects.create(comment_text="no",commenter_id=1,article_id=13,likes_num=0)
    Comment.objects.create(comment_text="no",commenter_id=2,article_id=14,likes_num=0)
    a.save()'''
    print((Comment.objects.filter(article_id=13)[0]).article_id)
    print((Article.objects.filter(article_id=1)[0]).author_id)
    add_comment("hello",1,1)
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
a = Article(article_id=1,
            author_id=1,
            article_text="wryyy",
            article_views=0,
            article_title="helloworld")
b = Comment(comment_text="no",commenter_id=1,article_id=13,likes_num=0)
c = Comment()
# Create your tests here.
if __name__=='__main__':
    b.save()
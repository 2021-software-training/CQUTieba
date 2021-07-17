'''
基于权值推荐的算法
记录每个文章的权值，存入大顶堆,取出最大的
'''
from django.test import TestCase
import sys
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CQUTieba.settings')
django.setup()
from search.maxheap import MaxHeap
from mainpage.models import Article
from random import  randint
class article_manage():
    def __init__(self,w,id):
        """
        :param w:此文的权值
        :param id: 此文的id
        """
        self.w = w
        self.id = id

    def __lt__(self,rhs):  #重载小于运算符
        return self.w<rhs.w

    def __le__(self,rhs):  #重载小于等于号
        return self.w<=rhs.w

    def __gt__(self,rhs):  #重载大于号
        return self.w>rhs.w

    def __ge__(self,rhs):  #重载大于等于号
        return self.w>=rhs.w
def weight_recommand():
    '''
    :return:当前热度最高的文章
    '''
    target = Article.objects.all()
    max_heap = MaxHeap()
    test,total = [],0
    for i in target:
        i.w = ((0.14*i.article_views/1000)+(0.24*(i.likes_num/15))+(0.62*i.comments_num))/max(1,i.regist_time)
        total += i.w
    for i in target:
        i.w += randint(0,int(total)-1)
        a=article_manage(i.w,i.article_id)
        test.append(a)
    max_heap.heapify(test)
    return max_heap.find_max().id
print(weight_recommand())

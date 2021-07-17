'''
依据标签的推荐,采集该用户点赞的文章,把他们的标签求并集,这个并集拿到所有文章中去拟合
找出最好拟合程度的两篇文章
'''
import random
from mainpage.models import LikeList
from mainpage.models import Article
from search.maxheap import *
from recommand.utils import most_like
def tag_recommand(user_id):
    num,return_article=0,[]  #返回了几个
    target = LikeList.objects.filter(user_id=user_id)  #查询出当中的点赞文章
    tags = set()
    for i in target:
        this_article = Article.objects.filter(article_id=i.article_id)
        tags.add(this_article[0].article_type1)
        tags.add(this_article[0].article_type2)
        tags.add(this_article[0].article_type3)
    tags = list(tags)#转化标签变成
    targets = Article.objects.all()
    max_heap=MaxHeap()
    tar=[]
    for i in targets:
        hash1=simhash(tags)
        hash2=simhash(cut(i.article_text))
        k=hash1.similarity(hash2)  #计算相似度
        if k==1:
            pass
        else:
            a=cosine_text(i.article_id,k)
            tar.append(a)
    max_heap.heapify(tar)
    temp = []
    for i in range(2):
        temp.append(max_heap.pop().id)
    return temp


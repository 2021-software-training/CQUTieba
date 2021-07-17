'''
基于内容推荐：
随机采取这位用户的点赞的两篇文章，直接从所有文章中，分别调取相似度最大的两篇文章
'''
import random

from mainpage.models import LikeList
from mainpage.models import Article
from search.maxheap import MaxHeap
from recommand.utils import most_like
def content_recommand(user_id):
    num,return_article = 0,[]#返回了几个
    target = LikeList.objects.filter(user_id = user_id)#查询出当中的点赞文章
    test = []#空列表
    for i in target:
        test.append(i)
    if len == 0:
        return num,return_article
    elif len(test) == 1:
        this_article_id = test[0].article_id#这篇id
        tar = Article.objects.filter(article_id = this_article_id)
        return_article.append(most_like(tar[0].article_text))
        num += 1
        return num,return_article
    else:
        a = random.randint(0,len(test)-1)
        b = random.randint(0,len(test)-1)
        while a==b:
            b = random.randint(0,len(test)-1)
        tar=Article.objects.filter(article_id=test[a].article_id)
        tar1=Article.objects.filter(article_id=test[b].article_id)
        return_article.append(most_like(tar[0].article_text))
        return_article.append(most_like(tar1[0].article_text))
        return 2,return_article
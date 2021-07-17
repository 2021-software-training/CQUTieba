
import sys
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CQUTieba.settings')
django.setup()
from search.maxheap import *
from mainpage.models import Article
from search.utils import *
def most_like(text):
    target = Article.objects.all()
    max_heap = MaxHeap()
    tar = []
    for i in target:
        hash1=simhash(cut(text))
        hash2=simhash(cut(i.article_text))
        k=hash1.similarity(hash2)  #计算相似度
        if k==1:
            pass
        else:
            a=cosine_text(i.article_id,k)
            tar.append(a)
    max_heap.heapify(tar)
    return max_heap.find_max().id
print(most_like("你好世界"))
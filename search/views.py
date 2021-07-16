from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from search.Ahocorasick import *
from mainpage.models import Article
from search.utils import cut,get_weight_and_keyword,simhash
from search.Ahocorasick import AhoCorasick
from math import log10
from search.maxheap import *
from math import sqrt
# Create your views here.
def Article_search(request):
    '''
    按照文章的标题或者文章的内容进行搜索
    1.标题：按照关键词全命中与
    2.文章内容：按照关键词的命中次数的数学期望值进行排序
    '''
    if request.method == 'GET':
        search_text = request.GET['searchText']#从前端抓取的搜索信息
        words_weight = get_weight_and_keyword(search_text)
        search_list,w = words_weight[0],words_weight[1]#提取关键词
        cutten_sentence = cut(search_text)
        ac = AhoCorasick(cutten_sentence)#建立起一个搜索类,在标题中检索所有可能的分词全部匹配的文章标题
        targets = Article.objects.all()
        temp,j = [],1
        temp1 = []
        for i in targets:
            ac.isin = 1 #不断的刷新
            ac.hit_num = 0
            temp_1 = {}
            ac.search(i.article_title,True)#返回各个文章的关键词检索情况
            if(ac.isin):#查验是否完成关键词全覆盖
                temp_1['article{0}'.format(j)] = i.article_title
                temp_1['hitnum'] = ac.hit_num
                temp_1['id'] = i.article_id#找出文章的的id
                temp.append(temp_1)
                j += 1
            ac.clear()#每一次完成清理
            '''
                以上为针对标题的进行处理
            '''
            ac.search(i.article_text,True)
            E_passage = 0
            E_passage1,E_passage2 = 0,0#向量化
            for i1 in range(len(w)):
                E_passage1 += pow(w[i1]*ac.num[search_list[i1]],2)
                E_passage2 += w[i1]*ac.num[search_list[i1]]
            if E_passage1 == 0:
                E_passage = 0
            else:
                E_passage = E_passage2/sqrt(E_passage1)
            if ac.isin == False and E_passage > 0:
                temp_1['article{0}'.format(j)]=i.article_title
                temp_1['E_passage']=E_passage
                temp_1['id']=i.article_id  #找出文章的的id
                temp1.append(temp_1)
                j+=1
            ac.clear()
        temp.sort(key = lambda a:a['hitnum'],reverse=True) #按照全覆盖，关键词命中率次数排序
        temp1.sort(key = lambda a:a['E_passage'],reverse=True)
        return JsonResponse(temp+temp1,safe=False,json_dumps_params={'ensure_ascii': False})
def Similar(request):
    '''
        基于本文的关键词提取+余弦相似度推荐出类似文章
        return {article1,....,articlen}
        一般来说，推荐出4篇文章即可
    '''
    if request.method == 'GET':
        mother_article = request.GET['article_text']#根据当前文章text来进行
        targets = Article.objects.all()#所有的文章的对象
        max_heap = MaxHeap() #建堆
        tar = []#列表检索
        for i in targets:
            hash1 = simhash(cut(mother_article))
            hash2 = simhash(cut(i.article_text))
            k = hash1.similarity(hash2)#计算相似度
            a = cosine_text(i.article_id,k)
            tar.append(a)
        max_heap.heapify(tar)
        temp = []
        for i in range(4):
            _id = max_heap.pop().id
            target = Article.objects.filter(article_id=_id)
            temp_1 = dict()
            temp_1['article{0}'.format(i)] = target[0].article_id
            temp.append(temp_1)
        return JsonResponse(temp,safe=False)
    return True


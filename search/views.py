from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from search.Ahocorasick import *
from mainpage.models import Article
from search.utils import cut
# Create your views here.
def Article_search(request):
    if request.method == 'GET':
        search_text = request.GET['searchText']#从前端抓取的搜索信息
        search_list = cut(search_text)
        ac = AhoCorasick(search_list)#建立起一个搜索类
        targets = Article.objects.all()
        temp,j = [],1
        for i in targets:
            ac.isin = 0
            temp_1 = {}
            ac.search(i.article_title,True)
            if(ac.isin):
                temp_1['article{0}'.format(j)] = i.article_title
                temp.append(temp_1)
                j += 1
        return JsonResponse(temp,safe=False,json_dumps_params={'ensure_ascii': False})




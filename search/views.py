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
            ac.search(i.article_title)
            if(ac.num):
                temp.append(i)
        return JsonResponse(temp,safe=False)




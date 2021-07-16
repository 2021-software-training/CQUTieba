from django.urls import path
from . import views

urlpatterns = [
    path('searcher/', views.Article_search, name='searcher'),  # 文章查询
    path('similar/', views.Similar, name='similar')  # 显示出相似的文章
]

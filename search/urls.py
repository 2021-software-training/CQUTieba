from django.urls import path
from . import views
urlpatterns = [
    path('searcher/',views.Article_search,name='searcher')#文章查询
]
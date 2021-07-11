from django.urls import path, include
from . import views

urlpatterns = [
    path('showAnArticle', views.show_an_article, name='show an article'),
    path('showAllArticle', views.show_all_articles, name='shou all article')
]

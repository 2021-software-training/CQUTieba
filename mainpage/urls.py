from django.urls import path, include
from . import views_article, views_user, views_comment, views_other

urlpatterns = [
    path('showAnArticle', views_article.show_an_article, name='show an article'),
    path('showAllArticle', views_article.show_all_articles, name='shou all article'),

    path('addComment', views_comment.add_comment, name='add comment'),

    path('addLike', views_other.add_like, name='add like')
]

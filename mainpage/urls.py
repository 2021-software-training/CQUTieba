from django.urls import path, include
from . import views_article, views_user, views_comment, views_other

urlpatterns = [
    path('addArticle', views_article.add_article, name='show an article'),
    path('editArticle', views_article.edit_article, name='show an article'),
    path('showAnArticle', views_article.show_an_article, name='show an article'),
    path('showPageAllArticles', views_article.show_page_all_articles, name='show an article'),
    path('showUserAllArticles', views_article.show_user_all_articles, name='shou all article'),

    path('addComment', views_comment.add_comment, name='add comment'),
    path('editComment', views_comment.edit_comment, name='edit comment'),
    path('showAllComment', views_comment.show_user_comment, name='show all comment'),

    path('getUserInfo', views_user.get_userinfo, name='get userinfo'),
    path('editUserInfo', views_user.edit_userinfo, name='edit userinfo'),


    path('addLikeArticle', views_other.add_like_article, name='add like article'),
    path('addLikeComment', views_other.add_like_comment, name='add like comment')
]

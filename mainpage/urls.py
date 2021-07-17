from django.urls import path, include
from . import views_article, views_user, views_comment, views_other, views_audio

urlpatterns = [
    path('addArticle', views_article.add_article, name='show an article'),
    path('editArticle', views_article.edit_article, name='show an article'),
    path('showAnArticle', views_article.show_an_article, name='show an article'),
    path('showPageAllArticles', views_article.show_page_all_articles, name='show an article'),
    path('showUserAllArticles', views_article.show_user_all_articles, name='shou all article'),

    path('addArticleComment', views_comment.add_article_comment, name='add article comment'),
    path('editComment', views_comment.edit_comment, name='edit comment'),
    path('showAllComment', views_comment.show_user_comment, name='show all comment'),

    path('getUserInfo', views_user.get_userinfo, name='get userinfo'),
    path('editUserInfo', views_user.edit_userinfo, name='edit userinfo'),
    path('changeHead', views_user.edit_profile, name='edit profile'),


    path('addLikeArticle', views_other.add_like_article, name='add like article'),
    path('addLikeComment', views_other.add_like_comment, name='add like comment'),
    path('getAnArticleComment', views_comment.show_article_comment, name='show article comment'),
    path('editProfile', views_user.edit_profile, name='edit profile'),

    path('audioArticle', views_audio.audio_article, name='audio article'),
    path('getImage/<str:username>', views_other.get_image, name='get image'),
    path('getAudio/<audio_id>', views_audio.get_audio, name='get audio'),
    path('editAudio', views_audio.edit_audio, name='edit audio'),
    path('getAudioInfo', views_audio.get_audio_info, name='get audio'),

    path('deleteArticle', views_article.delete_article, name='delete article'),
    path('deleteComment', views_other.delete_comment, name='delete comment')
]

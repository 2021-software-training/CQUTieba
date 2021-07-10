from django.urls import path, include
from . import views

urlpatterns = [
    path('addArticle', views.add_article, 'add_article'),
    path('addComment', views.add_comment, 'add_comment')
]

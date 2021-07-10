from django.urls import path, include
from . import views

urlpatterns = [
    path('showAnArticle', views.show_an_article, 'add_article')
]

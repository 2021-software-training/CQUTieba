from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.return_json, name='return_json'),

    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('search_user',views.user_search,name='search_user')
]
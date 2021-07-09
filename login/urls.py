from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.return_json, name='return_json'),
    path('login', views.login, name='login'),
    path('regist', views.register, name='email_sender'),
    path('testget', views.func1, name='func1'),
    path('testpost', views.func2, name='func1')
]

from django.urls import  path
from . import  views
urlpatterns = [
   path('',views.main,name="main"),
   path('main1',views.main1,name="main1"),
   path('email_sender/<str:code>')
]

from django.urls import  path
from . import  views
urlpatterns = [
   path('dir',views.email_dir),
   path('<str:code>',views.email_op,name='code')
]

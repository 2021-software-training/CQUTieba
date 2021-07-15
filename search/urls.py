from django.urls import path
from . import views
urlpatterns = [
    path('searcher/',views.searcher,name='searcher')
]

from django.urls import path
from . import views
from . import feeds
urlpatterns = [
    #path('', views.feed_list, name='feed_list'),
    #path("entries/", feeds.AddFeed()),
    path('', views.index, name='index'),
    #path('', views.index, name='upload'),
]
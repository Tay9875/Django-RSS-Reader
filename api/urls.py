from django.urls import path
from . import views

urlpatterns = [
    path('feeds/',views.getFeedData),
    path('feeds/items/',views.getFeedItemData),
    path('feeds/add/',views.addFeedData),
    path('feeds/<int:pk>/',views.specificFeed),
    path('feeds/<int:pk>/items/',views.specificFeedItem),
]
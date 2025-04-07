from django.urls import path
from . import views

urlpatterns = [
    path('subscriptions/', views.user_subscriptions, name='user_subscriptions'),
]
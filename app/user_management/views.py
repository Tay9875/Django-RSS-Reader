from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def user_subscriptions(request):
    return HttpResponse("User Subscriptions")
from django.shortcuts import render
from .feeds import Feed, FeedItem
from .forms import RssForm
import requests
from .tasks import updatefeeds
from .feeds import BuildFeed
from api.views import addFeedData

def upload_url(request):
    #add = AddFeed()
    if request.POST:
        form = RssForm(request.POST)
        print(form.fields)
        #if form.is_valid():
        #add = AddFeed()
            #if add.is_valid():
                #add.save()
            #return HttpResponseRedirect("/thanks/")
    #else:
        #form = RssForm(request.POST)

    #return render(request, "index.html", {'form': form})

def index(request):
    updatefeeds(repeat=3600)
    form = RssForm(request.POST or None)
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            # Effectuer une requête POST à l'API
            response = requests.post('http://127.0.0.1:8000/api/feeds/add/', json={'url': url})
            if response.status_code == 201:
                print("Feed successfully added")
            else:
                print("Error in feed 'adding'", response.content)

    #form = RssForm(request.POST)
    #if request.POST:
        #print(request.POST.get('url'))
        #add = BuildFeed(url=request.POST.get('url'))
        # if form.is_valid():
        # add = AddFeed()

    #feeds_list = Feed.objects.order_by("title")
    #feeditems_list = FeedItem.objects.order_by("published_date")
    return render(request, 'posts/index.html',{'form': form})
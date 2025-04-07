from api.views import format_date
from background_task import background
from .models import Feed, FeedItem
import feedparser

@background(schedule=60*60)  # Exécuter toutes les heures
def updatefeeds():
    feeds = Feed.objects.all()
    for feed in feeds:
        f = feedparser.parse(feed.url)
        formatted_date = format_date(f.feed.updated)

        for entry in f.entries:
            published_date = format_date(entry.get('published'))
            data = {'feed': feed,'title': entry.title,'link': entry.link,'desc': entry.description if 'description' in entry else '','published_date': published_date}
            item, created = FeedItem.objects.update_or_create(feed=feed, link=entry.link, defaults=data)
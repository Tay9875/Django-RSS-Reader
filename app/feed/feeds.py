from datetime import datetime

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from . models import Feed, FeedItem
import feedparser
from django.utils import timezone

#Si on cherchait a emplacer API
class BuildFeed(Feed):
    def __init__(self, url):
        self.url = url
        try:
            feed = feedparser.parse(self.url)
            formatted_date = self.format_date(feed.feed.updated)
            f = Feed(url=feed.feed.link, title=feed.feed.title, desc=feed.feed.description, last_fetched=formatted_date)
            f.save()
            for entry in feed.entries:
                published_date = self.format_date(entry.published)
                e = FeedItem(feed=f, title=entry.title, link=entry.link, desc=entry.description, published_date=published_date)
                e.save()
        except ValueError as e:
            print(f"Data error : {e}")
            return None

    def format_date(self, date_str):
        try:
            date_object = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            # Formater la date au format attendu
            formatted_date = date_object.strftime("%Y-%m-%d %H:%M:%S%z")
            return formatted_date
        except ValueError as e:
            print(f"Datetime formatting error : {e}")
            return None

    def PrintUrl(self):
        print(self.url)
    #title = "Police beat site news"
    #link = "/sitenews/"
    #description = "Updates on changes and additions to police beat central."
    #url = "https://www.lemonde.fr/rss/une.xml"
    #feed = feedparser.parse(url)
    #print(feed.feed.title)
    #print(feed.feed.link)
    #print(feed.feed.description)
    #f = Feed(url=feed['href'],title='Le Monde',desc="L'Actualité internationale")
    #for entry in feed.entries:
        #print(entry.keys())
        #e = FeedItem(feed=f,title=entry['title'], link=entry['link'], desc=entry['description'], published_date=entry['published'])

#class LatestEntriesFeeds(Feed):
    #title = "Tutorials"
    #link = "/latesttutorials/"
    #description = "Recent free tutorials on LearnDjango.com."

    #def items(self):
        #return LatestEntriesFeeds.objects.order_by("-updated_at")[:100]

    #def item_title(self, item):
        #return item.title

    #def item_description(self, item):
        #return truncatewords(item.content, 100)

    #def item_lastupdated(self, item):
        #return item.updated_at
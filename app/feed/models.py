import datetime
from django.db import models
from django.utils import timezone

class Feed(models.Model):
    url = models.CharField(max_length=2048)
    title = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    last_fetched = models.DateTimeField()

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.last_fetched >= timezone.now() - datetime.timedelta(days=1)

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2048)
    desc = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField()
    def __str__(self):
        return self.title

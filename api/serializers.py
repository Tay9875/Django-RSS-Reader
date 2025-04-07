from rest_framework import serializers
from app.feed.models import Feed, FeedItem

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

class FeedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedItem
        fields = '__all__'
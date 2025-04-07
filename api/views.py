from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from app.feed.models import Feed, FeedItem
from .serializers import FeedSerializer, FeedItemSerializer
import feedparser
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def getFeedData(request):
    feeds = Feed.objects.all()
    serializer = FeedSerializer(feeds, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addFeedData(request):
    url = request.data.get('url')
    if not url:
        return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        feed = feedparser.parse(url)
        formatted_date = format_date(feed.feed.updated)

        feed_data = {'url': feed.feed.link,'title': feed.feed.title,'desc': feed.feed.description,'last_fetched': formatted_date}
        serializer = FeedSerializer(data=feed_data)
        if serializer.is_valid():
            f = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for entry in feed.entries:
            published_date = format_date(entry.get('published'))
            item_data = {'feed': f.id,'title': entry.title,'link': entry.link,'desc': entry.description if 'description' in entry else '','published_date': published_date}
            item_serializer = FeedItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item_serializer.save()
            else:
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Feed added successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Data error: {e}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except (ValueError, TypeError):
        return None
    #feed = feedparser.parse(request.data)
    #print("REQUEST -------------------------------",request.data)
    #serializer = FeedSerializer(data=request.data)
    #if serializer.is_valid():
        #serializer.save()
        #return Response(serializer.data, status=status.HTTP_201_CREATED)
    #return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
@permission_classes([AllowAny])
def specificFeed(request, pk):
    try:
        feed = Feed.objects.get(pk=pk)
    except Feed.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FeedSerializer(feed)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FeedSerializer(feed, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        feedItems = FeedItem.objects.filter(feed=feed)
        #feedItems.delete()
        #feed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getFeedItemData(request):
    search_query = request.GET.get('search', '')
    feeditems = FeedItem.objects.all()

    if search_query:
        feeditems = feeditems.filter(title__icontains=search_query) | feeditems.filter(desc__icontains=search_query)

    serializer = FeedItemSerializer(feeditems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addFeedItemData(request):
    serializer = FeedItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def specificFeedItem(request, pk):
    try:
        feed = Feed.objects.get(pk=pk)
        feedItems = FeedItem.objects.filter(feed=feed)
    except Feed.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FeedItemSerializer(feedItems,many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_204_NO_CONTENT)
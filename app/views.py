from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Tweet

def home_view(request):
    return render(request, 'home.html', {})

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    return HttpResponse(f"<h1>Hello {tweet_id} - {obj.content}</h1>")

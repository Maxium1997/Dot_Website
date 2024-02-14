import requests

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from isodate import parse_duration

# Create your views here.


class PlaygroundView(TemplateView):
    template_name = 'playground/index.html'


class KaraokeView(TemplateView):
    template_name = 'playground/karaoke/index.html'


def search_index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': 'karaoke ' + request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }

        video_ids = []
        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet, contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 9,
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': 'https://www.youtube.com/watch?v={video_id}'.format(video_id=result['id']),
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'playground/karaoke/search/index.html', context)

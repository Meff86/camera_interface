from django.urls import path
from .views import index, stream_video

urlpatterns = [
    path('', index, name='index'),
    path('video_feed/', stream_video, name='stream_video'),
]

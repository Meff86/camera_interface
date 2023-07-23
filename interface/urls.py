from django.urls import path
from . import views



app_name = "interface"

urlpatterns = [
    path('digital_camera/', views.digital_camera, name='digital_camera'),
    path('video_feed/', views.stream_video, name='stream_video'),
    path('save_screenshot/', views.save_screenshot, name='save_screenshot'),
    path('example_view/', views.example_view, name='example_view'),
    path('capture_frames/', views.capture_frames, name='capture_frames'),
    path('send_files/', views.send_files_to_server, name='send_files'),
]

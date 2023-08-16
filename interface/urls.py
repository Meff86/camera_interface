from django.urls import path
from . import views



app_name = "interface"

urlpatterns = [
    path('digital_camera/', views.digital_camera, name='digital_camera'),
    path('stream_video/', views.stream_video, name='stream_video'),
    path('save_screenshot/', views.save_screenshot, name='save_screenshot'),
    path('example_view/', views.example_view, name='example_view'),
    path('capture_frames/', views.capture_frames, name='capture_frames'),
    path('send_files/', views.send_files_to_server, name='send_files'),
    path('control/', views.control_page, name='control_page'),
    path('save_car_part/', views.save_car_part, name='save_car_part'),
    path('get_photos_by_article/', views.get_photos_by_article, name='get_photos_by_article'),
    path('roster_page/', views.roster_page, name='roster_page'),
    path('roster_page/<str:selected_date>/', views.roster_page, name='roster_page_with_date'),
    path('get_car_parts_json/', views.get_car_parts_json, name='get_car_parts_json'),
    path('delete_matching_article/', views.delete_matching_article_view, name='delete_matching_article'),
    # ...

]

from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.login_view, name='login'),
    # Другие URL-шаблоны вашего приложения
]
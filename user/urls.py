from django.urls import path
from . import views
from .views import logout_view

app_name = 'user'
urlpatterns = [
    path('', views.login_view, name='login'),
    # Другие URL-шаблоны вашего приложения
    path('logout/', logout_view, name='logout'),
]


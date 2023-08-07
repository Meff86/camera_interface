from django.contrib import admin
from .models import CarPart, Photo

@admin.register(CarPart)
class CarPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'article_number')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('car_part', 'image_url')

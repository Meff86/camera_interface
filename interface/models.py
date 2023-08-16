from django.db import models
from datetime import datetime


class CarPart(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    article_number = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    place = models.CharField(max_length=50, verbose_name='Место', default='')
    added_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    def matching_articles(self):
        return MatchingArticle.objects.filter(article_number=self.article_number)

    def all_photos(self):
        photos = Photo.objects.filter(car_part__article_number=self.article_number)
        matching_articles = self.matching_articles()
        for ma in matching_articles:
            photos |= Photo.objects.filter(car_part__article_number=ma.article_number)
        return photos

class MatchingArticle(models.Model):
    article_number = models.CharField(max_length=50, unique=True)
    added_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.article_number


class Photo(models.Model):
    car_part = models.ForeignKey(CarPart, on_delete=models.CASCADE, related_name='photos', verbose_name='Запчасть')
    image_url = models.URLField(max_length=200, verbose_name='URL фотографии', default='')

    def __str__(self):
        return f"Фото {self.car_part.name}"


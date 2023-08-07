from django.db import models


class CarPart(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    article_number = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    place = models.CharField(max_length=50, verbose_name='Место', default='')

    def __str__(self):
        return self.name


class Photo(models.Model):
    car_part = models.ForeignKey(CarPart, on_delete=models.CASCADE, related_name='photos', verbose_name='Запчасть')
    image_url = models.URLField(max_length=200, verbose_name='URL фотографии', default='')

    def __str__(self):
        return f"Фото {self.car_part.name}"

# Generated by Django 4.2.3 on 2023-08-10 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0004_carpart_added_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchingArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_number', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]

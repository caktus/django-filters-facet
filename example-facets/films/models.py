from django.db import models


class Film(models.Model):
    show_id = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    director = models.CharField(max_length=1000)
    cast = models.TextField()
    country = models.CharField(max_length=1000)
    date_added = models.DateField()
    release_year = models.DateField()
    rating = models.CharField(max_length=15)
    duration = models.CharField(max_length=1000)
    listed_in = models.TextField()
    description = models.TextField(default="")

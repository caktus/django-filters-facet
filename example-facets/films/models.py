from django.db import models


class Film(models.Model):
    show_id = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    cast = models.TextField()
    country = models.CharField(max_length=25)
    date_added = models.DateField()
    release_year = models.DateField()
    rating = models.CharField(max_length=15)
    duration = models.CharField(max_length=100)
    listed_in = models.TextField()
    description = models.TextField(default="")

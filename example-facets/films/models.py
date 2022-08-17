from django.db import models
# need a tuple for cast?
# need a tuplse for rating?
# need a choice for rating?
# TYPE = (
#     (1, "Movie"),
#     (2, "TV Show")
# )

# RATING = (
#     (1, "R"),
#     (2, "TV-MA"),
#     (3, "NC-17"),
#     (4, "PG-13"),
#     (5, "TV-14"),
#     (6, "TV-Y"),
#     (7, "TV-Y7"),
#     (8, "G"),
#     (9, "TV-G"),
#     (10, "PG"),
#     (11, "TV-PG"),
# )
# Create your models here.
class films(models.Model):
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
    description = models.TextField()
  
# class films(models.Model):
#     show_id = models.PositiveIntegerField(primary_key=True)
#     type = models.PositiveSmallIntegerField(choices=TYPE)
#     title = models.CharField(max_length=100)
#     director = models.CharField(max_length=100)
#     cast = models.TextField()
#     country = models.CharField(max_length=25)
#     date_added = models.DateField()
#     release_year = models.DateField()
#     rating = models.PositiveSmallIntegerField(choices=RATING)
#     duration = models.DurationField()
#     listed_in = models.TextField()
#     description = models.TextField()
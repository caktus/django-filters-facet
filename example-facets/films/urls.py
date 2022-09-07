from django.urls import path

from . import views

urlpatterns = [
    path("", views.FilmListView.as_view(), name="films-list"),
    path("manual/", views.ManualFilmListView.as_view(), name="manual-films-list"),
]

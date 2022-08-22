from django.urls import path

from . import views

urlpatterns = [
    path("", views.FilmListView.as_view(), name="film-list"),
]

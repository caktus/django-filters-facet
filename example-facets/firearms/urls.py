from django.urls import path

from . import views

urlpatterns = [
    path("", views.StatuteListView.as_view(), name="statute-list"),
]

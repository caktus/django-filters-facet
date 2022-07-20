from django.urls import path

from . import views

urlpatterns = [
    path("", views.StopListView.as_view(), name="stop-list"),
]

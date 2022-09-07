from django.db.models import Count
from django.views.generic.list import ListView

from .filters import FilmFilterSet, SimpleFilmFilterSet
from .models import Film


class FilmListView(ListView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    model = Film
    ordering = "title"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_set = FilmFilterSet(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter_set
        return context


class ManualFilmListView(ListView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    model = Film
    paginate_by = 5
    template_name_suffix = "_list_manual"

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_set = SimpleFilmFilterSet(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["film_types"] = (
            self.get_queryset().values("type").annotate(count=Count("id"))
        )
        return context

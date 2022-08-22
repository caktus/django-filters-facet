# from django.db.models import Case, F, FilteredRelation, Q, Value, When
from django.views.generic.list import ListView

# from .filters import FilmFilterSet
from .models import Film


class FilmListView(ListView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    model = Film
    ordering = "title"
    paginate_by = 25

    def get_queryset(self):
        return super.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["filter"] = self.filter_set
        return context

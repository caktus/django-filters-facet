# from django.db.models import Case, F, FilteredRelation, Q, Value, When
from django.views.generic.list import ListView

from .filters import StatuteFilterSet
from .models import Statute


class StatuteListView(ListView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    model = Statute
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_set = StatuteFilterSet(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter_set
        return context

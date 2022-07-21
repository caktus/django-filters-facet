from django.views.generic.list import ListView

from .filters import StopFilterSet
from .models import Stop


class StopListView(ListView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    model = Stop
    ordering = "-date"
    paginate_by = 25

    def get_queryset(self):
        self.filter_set = StopFilterSet(
            self.request.GET, queryset=super().get_queryset()
        )
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter_set
        return context

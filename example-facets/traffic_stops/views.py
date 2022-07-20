from django.views.generic.list import ListView

from .models import Stop


class StopListView(ListView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    model = Stop
    ordering = "-date"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

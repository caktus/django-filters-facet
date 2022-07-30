from django.db.models import F, FilteredRelation, Q, ExpressionWrapper
from django.db.models import Case, Value, When
from django.db import models

from django.views.generic.list import ListView

from .filters import StopFilterSet
from .models import Stop, Person, SEARCH_TYPE_CHOICES


class StopListView(ListView):
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    model = Stop
    ordering = "-date"
    paginate_by = 25

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .annotate(
                driver=FilteredRelation(
                    "person",
                    condition=Q(person__type="D"),
                ),
                driver_search=FilteredRelation(
                    "search",
                    condition=Q(search__driver_search=True),
                ),
                driver_race=Case(
                    When(
                        driver__ethnicity=Person.Ethnicity.HISPANIC,
                        then=Value(Person.Race.HISPANIC.label),
                    ),
                    When(
                        driver__ethnicity=Person.Ethnicity.NON_HISPANIC,
                        driver__race=Person.Race.ASIAN,
                        then=Value(Person.Race.ASIAN.label),
                    ),
                    When(
                        driver__ethnicity=Person.Ethnicity.NON_HISPANIC,
                        driver__race=Person.Race.BLACK,
                        then=Value(Person.Race.BLACK.label),
                    ),
                    When(
                        driver__ethnicity=Person.Ethnicity.NON_HISPANIC,
                        driver__race=Person.Race.NATVE_AMERICAN,
                        then=Value(Person.Race.NATVE_AMERICAN.label),
                    ),
                    When(
                        driver__ethnicity=Person.Ethnicity.NON_HISPANIC,
                        driver__race=Person.Race.OTHER,
                        then=Value(Person.Race.OTHER.label),
                    ),
                    When(
                        driver__ethnicity=Person.Ethnicity.NON_HISPANIC,
                        driver__race=Person.Race.WHITE,
                        then=Value(Person.Race.WHITE.label),
                    ),
                    default=Value("???"),
                ),
            )
            .annotate(
                search_type=F("driver_search__type"),
                driver_gender=F("driver__gender"),
            )
        )
        self.filter_set = StopFilterSet(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter_set
        return context

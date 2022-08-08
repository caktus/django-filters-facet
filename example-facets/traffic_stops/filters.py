import django_filters

from django_filters_facet import Facet, FacetedFilterSet

from .models import GENDER_CHOICES, SEARCH_TYPE_CHOICES, Stop


class StopFilterSet(FacetedFilterSet):
    search_type = django_filters.ChoiceFilter(
        field_name="driver_search__type",
        choices=SEARCH_TYPE_CHOICES,
        null_label="Not Searched",
        label="search type",
    )
    driver_race = django_filters.CharFilter(label="Driver Race")
    driver_gender = django_filters.ChoiceFilter(
        label="Driver Gender", choices=GENDER_CHOICES
    )

    class Meta:
        model = Stop
        fields = ["agency", "driver_race", "driver_gender", "agency", "purpose"]

    def configure_facets(self):
        self.filters["agency"].facet = Facet()
        self.filters["driver_race"].facet = Facet()
        self.filters["driver_gender"].facet = Facet()
        self.filters["purpose"].facet = Facet()
        self.filters["search_type"].facet = Facet()

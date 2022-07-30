import django_filters

from .models import Stop, SEARCH_TYPE_CHOICES
from django_filters_facet import Facet, FacetedFilterSet


class StopFilterSet(FacetedFilterSet):
    search_type = django_filters.ChoiceFilter(
        field_name="driver_search__type",
        choices=SEARCH_TYPE_CHOICES,
        null_label="Not Searched",
        label="search type",
    )
    driver_race = django_filters.CharFilter(label="Driver Race")

    class Meta:
        model = Stop
        fields = ["agency", "purpose"]

    def configure_facets(self):
        self.filters["agency"].facet = Facet()
        self.filters["driver_race"].facet = Facet()
        self.filters["purpose"].facet = Facet()
        self.filters["search_type"].facet = Facet()

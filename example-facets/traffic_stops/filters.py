import django_filters

from .models import Stop
from django_filters_facet import Facet, FacetedFilterSet


class StopFilterSet(FacetedFilterSet):
    search_type = django_filters.ChoiceFilter(
        choices=Stop.SEARCH_TYPE_CHOICES,
        null_label="Not Searched",
    )

    class Meta:
        model = Stop
        fields = ["driver_gender", "stop_purpose"]

    def configure_facets(self):
        self.filters["stop_purpose"].facet = Facet()
        self.filters["search_type"].facet = Facet()
        self.filters["driver_gender"].facet = Facet()

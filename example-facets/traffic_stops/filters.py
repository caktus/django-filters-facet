import django_filters

from .models import Stop
from django_filters_facet import Facet, FacetedFilterSet


class StopFilterSet(FacetedFilterSet):
    stop_purpose = django_filters.ChoiceFilter(choices=Stop.PURPOSE_CHOICES)

    class Meta:
        model = Stop
        fields = ["stop_purpose"]

    def configure_facets(self):
        self.filters["stop_purpose"].facet = Facet()

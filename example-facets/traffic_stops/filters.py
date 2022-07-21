from .models import Stop
from django_filters_facet import Facet, FacetedFilterSet


class StopFilterSet(FacetedFilterSet):
    class Meta:
        model = Stop
        fields = ["stop_purpose", "search_type"]

    def configure_facets(self):
        self.filters["stop_purpose"].facet = Facet()
        self.filters["search_type"].facet = Facet()

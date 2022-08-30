from django_filters_facet import Facet, FacetedFilterSet

from .models import Film


class FilmFilterSet(FacetedFilterSet):
    class Meta:
        model = Film
        fields = ["type", "release_year", "rating", "listed_in"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()
        self.filters["release_year"].facet = Facet()
        self.filters["rating"].facet = Facet()
        self.filters["listed_in"].facet = Facet()

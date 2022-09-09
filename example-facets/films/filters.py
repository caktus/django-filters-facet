import django_filters

from django.contrib.postgres import search

from django_filters_facet import Facet, FacetedFilterSet

from .models import Film


class FilmFilterSet(FacetedFilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Film
        fields = ["type", "genres"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()
        self.filters["genres"].facet = Facet()

    def filter_search(self, queryset, name, value):
        vector = (
            search.SearchVector("title", weight="A")
            + search.SearchVector("description", weight="B")
            + search.SearchVector("director", weight="B")
            + search.SearchVector("cast", weight="B")
            + search.SearchVector("country", weight="C")
        )
        query = search.SearchQuery(value, search_type="websearch")
        return (
            queryset.annotate(
                search=vector,
                rank=search.SearchRank(vector, query),
            )
            .filter(search=query)
            .order_by("-rank")
        )


class SimpleFilmFilterSet(FacetedFilterSet):
    class Meta:
        model = Film
        fields = ["type"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()

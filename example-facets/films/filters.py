import django_filters

from django.contrib.postgres import search

from django_filters_facet import Facet, FacetedFilterSet

from .models import Film


class FilmFilterSet(FacetedFilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Film
        fields = ["type", "release_year", "rating", "listed_in"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()
        self.filters["release_year"].facet = Facet()
        self.filters["rating"].facet = Facet()
        self.filters["listed_in"].facet = Facet()

    def filter_search(self, queryset, name, value):
        vector = search.SearchVector("description", weight="B")
        query = search.SearchQuery(value)
        return (
            queryset.annotate(
                rank=search.SearchRank(vector, query),
                headline=search.SearchHeadline(
                    "description",
                    query,
                    min_words=30,
                    start_sel="<mark>",
                    stop_sel="</mark>",
                ),
            )
            .filter(rank__gt=0.1)
            .order_by("-rank")
        )

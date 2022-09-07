import django_filters

from django.contrib.postgres import search

from django_filters_facet import Facet, FacetedFilterSet

from .models import Film


class FilmFilterSet(FacetedFilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")
    listed_in = django_filters.CharFilter(label="Genre")

    class Meta:
        model = Film
        fields = ["type", "release_year", "rating", "listed_in"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()
        self.filters["release_year"].facet = Facet()
        self.filters["rating"].facet = Facet()
        self.filters["listed_in"].facet = Facet()

    def filter_search(self, queryset, name, value):
        vector = (
            search.SearchVector("title", weight="A")
            + search.SearchVector("description", weight="A")
            + search.SearchVector("director", weight="B")
            + search.SearchVector("cast", weight="B")
            + search.SearchVector("country", weight="C")
        )
        query = search.SearchQuery(value)
        return (
            queryset.annotate(
                rank=search.SearchRank(vector, query),
                headline=search.SearchHeadline(
                    "description",
                    query,
                    min_words=6,
                    start_sel="<mark>",
                    stop_sel="</mark>",
                ),
            )
            .filter(rank__gt=0.1)
            .order_by("-rank")
        )


class SimpleFilmFilterSet(FacetedFilterSet):
    class Meta:
        model = Film
        fields = ["type"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()

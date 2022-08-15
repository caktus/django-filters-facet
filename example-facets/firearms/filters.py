import django_filters

from django.contrib.postgres import search

from django_filters_facet import Facet, FacetedFilterSet

from .models import Statute


class StatuteFilterSet(FacetedFilterSet):
    search = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Statute
        fields = ["subjects", "jurisdictions"]

    def configure_facets(self):
        self.filters["subjects"].facet = Facet(order_by="subjects__name")
        self.filters["jurisdictions"].facet = Facet(order_by="jurisdictions__name")

    def filter_search(self, queryset, name, value):
        vector = search.SearchVector("summary", weight="B")
        query = search.SearchQuery(value)
        return (
            queryset.annotate(
                rank=search.SearchRank(vector, query),
                headline=search.SearchHeadline(
                    "summary",
                    query,
                    min_words=30,
                    start_sel="<mark>",
                    stop_sel="</mark>",
                ),
            )
            .filter(rank__gt=0.1)
            .order_by("-rank")
        )

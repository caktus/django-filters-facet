# import django_filters

from django_filters_facet import Facet, FacetedFilterSet

from .models import Film


class FilmFilterSet(FacetedFilterSet):
    # search_type = django_filters.ChoiceFilter(
    #     field_name="driver_search__type",
    #     choices=SEARCH_TYPE_CHOICES,
    #     null_label="Not Searched",
    #     label="search type",
    # )
    # driver_race = django_filters.CharFilter(label="Driver Race")
    # driver_gender = django_filters.ChoiceFilter(
    #     label="Driver Gender", choices=GENDER_CHOICES
    # )

    class Meta:
        model = Film
        fields = ["type", "release_year", "rating", "listed_in"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()
        self.filters["release_year"].facet = Facet()
        self.filters["rating"].facet = Facet()
        self.filters["listed_in"].facet = Facet()

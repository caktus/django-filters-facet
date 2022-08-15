import django_filters

from django.db.models.functions import ExtractYear

from django_filters_facet import Facet, FacetedFilterSet

from .models import Student


class StudentFilterSet(FacetedFilterSet):
    year = django_filters.NumberFilter(
        field_name="dob",
        lookup_expr="year",
        label="Year born",
    )

    class Meta:
        model = Student
        fields = ["grade", "name", "classes"]

    def configure_facets(self):
        self.filters["grade"].facet = Facet()
        self.filters["year"].facet = Facet(
            queryset=lambda qs: qs.annotate(year=ExtractYear("dob")),
            group_by_filter_name=True,
        )
        self.filters["classes"].facet = Facet()

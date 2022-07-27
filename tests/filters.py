from django.db.models.functions import ExtractYear

import django_filters
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
        fields = ["grade"]

    def configure_facets(self):
        self.filters["grade"].facet = Facet()
        self.filters["year"].facet = Facet(
            queryset=lambda qs: qs.annotate(year=ExtractYear("dob"))
        )

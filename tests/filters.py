from django_filters_facet import Facet, FacetedFilterSet

from .models import Student


class StudentFilterSet(FacetedFilterSet):
    class Meta:
        model = Student
        fields = ["grade"]

    def configure_facets(self):
        self.filters["grade"].facet = Facet()

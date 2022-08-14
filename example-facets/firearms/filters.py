from django_filters_facet import Facet, FacetedFilterSet

from .models import Statute


class StatuteFilterSet(FacetedFilterSet):
    class Meta:
        model = Statute
        fields = ["subjects", "jurisdictions"]

    def configure_facets(self):
        self.filters["subjects"].facet = Facet(order_by="subjects__name")
        self.filters["jurisdictions"].facet = Facet(order_by="jurisdictions__name")

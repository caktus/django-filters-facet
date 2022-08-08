import django_filters


class FacetedFilterSet(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attach_facets()

    def attach_facets(self):
        for filter_ in self.filters.values():
            if not hasattr(filter_, "facet"):
                filter_.facet = None
        self.configure_facets()
        # provide reference back to filter through facet
        for filter_field_name, filter_ in self.filters.items():
            if filter_.facet:
                filter_.filter_field_name = filter_field_name
                filter_.facet.filter = filter_

    def configure_facets(self):
        raise NotImplementedError("Must implement configure_facets in subclass")

    def get_facets(self):
        for filter_ in self.filters.values():
            if filter_.facet:
                yield filter_.facet

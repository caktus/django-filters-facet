from django_filters_facet import Facet

from .filters import StudentFilterSet


class TestFacet:
    def test_property_form(self):
        fs = StudentFilterSet()
        fs.filters["grade"].facet = Facet()
        fs.attach_facets()
        assert fs.filters["grade"].facet.form == fs.filters["grade"].parent.form

    def test_property_form_field(self):
        fs = StudentFilterSet()
        fs.filters["grade"].facet = Facet()
        fs.attach_facets()
        assert (
            fs.filters["grade"].facet.form.fields["grade"]
            == fs.filters["grade"].parent.form.fields["grade"]
        )

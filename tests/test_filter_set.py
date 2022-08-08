import pytest

from django.db.models import Q

from django_filters_facet import Facet

from .factories import StudentFactory
from .filters import StudentFilterSet
from .models import Student


class TestAttachFacets:
    def test_facet_links_to_filter(self):
        fs = StudentFilterSet(queryset=Student.objects.all())
        fs.filters["grade"].facet = Facet()
        fs.attach_facets()
        assert fs.filters["grade"].facet.filter == fs.filters["grade"]

    def test_saved_filter_field_name(self):
        fs = StudentFilterSet(queryset=Student.objects.all())
        fs.filters["grade"].facet = Facet()
        fs.attach_facets()
        assert fs.filters["grade"].facet.filter.filter_field_name == "grade"


@pytest.mark.django_db
class TestChoicesField:
    def test_default_facet_counts(self):
        StudentFactory(grade=Student.Grade.FIRST)
        StudentFactory(grade=Student.Grade.SECOND)
        StudentFactory(grade=Student.Grade.SECOND)
        f = StudentFilterSet(queryset=Student.objects.all())
        expected = [
            {"count": 2, "is_active": False, "label": "2nd", "value": 2},
            {"count": 1, "is_active": False, "label": "1st", "value": 1},
        ]
        assert list(f.filters["grade"].facet.items_for_display()) == expected

    def test_facet_exclude(self):
        StudentFactory(grade=Student.Grade.FIRST)
        StudentFactory(grade=Student.Grade.SECOND)
        StudentFactory(grade=Student.Grade.SECOND)
        f = StudentFilterSet(queryset=Student.objects.all())
        f.filters["grade"].facet.exclude = Q(grade=Student.Grade.FIRST)
        expected = [
            {"count": 2, "is_active": False, "label": "2nd", "value": 2},
        ]
        assert list(f.filters["grade"].facet.items_for_display()) == expected

    def test_facet_exclude_everything(self):
        StudentFactory(grade=Student.Grade.FIRST)
        f = StudentFilterSet(
            {"grade": Student.Grade.FIRST}, queryset=Student.objects.all()
        )
        f.filters["grade"].facet.exclude = Q(grade=Student.Grade.FIRST)
        expected = [
            {"count": 0, "is_active": True, "label": "1st", "value": 1},
        ]
        assert list(f.filters["grade"].facet.items_for_display()) == expected


@pytest.mark.django_db
class TestBirthYearField:
    def test_foo(self):
        StudentFactory(dob="1985-07-20")
        StudentFactory(dob="1987-04-02")
        StudentFactory(dob="1987-11-01")
        f = StudentFilterSet()
        expected = [
            {"count": 2, "is_active": False, "label": 1987, "value": 1987},
            {"count": 1, "is_active": False, "label": 1985, "value": 1985},
        ]
        assert list(f.filters["year"].facet.items_for_display()) == expected

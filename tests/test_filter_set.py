from django.db.models import Q

import pytest

from .factories import StudentFactory
from .filters import StudentFilterSet
from .models import Student


@pytest.mark.django_db
class TestChoicesField:
    def test_default_facet_counts(self):
        StudentFactory(grade=Student.Grade.FIRST)
        StudentFactory(grade=Student.Grade.SECOND)
        StudentFactory(grade=Student.Grade.SECOND)
        f = StudentFilterSet({}, queryset=Student.objects.all())
        expected = [
            {"count": 2, "is_active": False, "label": "2nd", "value": 2},
            {"count": 1, "is_active": False, "label": "1st", "value": 1},
        ]
        assert list(f.filters["grade"].facet.items_for_display()) == expected

    def test_facet_exclude(self):
        StudentFactory(grade=Student.Grade.FIRST)
        StudentFactory(grade=Student.Grade.SECOND)
        StudentFactory(grade=Student.Grade.SECOND)
        f = StudentFilterSet({}, queryset=Student.objects.all())
        f.filters["grade"].facet.exclude = Q(grade=Student.Grade.FIRST)
        expected = [
            {"count": 2, "is_active": False, "label": "2nd", "value": 2},
        ]
        assert list(f.filters["grade"].facet.items_for_display()) == expected

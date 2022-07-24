import pytest

from django_filters_facet import __version__

from .factories import SchoolFactory


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.django_db
def test_foo():
    assert SchoolFactory().name != ""

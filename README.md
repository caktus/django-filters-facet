# django-filters-facet

django-filters-facet is a
[django-filter](https://pypi.org/project/django-filter/) extension to refine
search results using faceted navigation functionality.

[![test](https://github.com/caktus/django-filters-facet/actions/workflows/test.yaml/badge.svg)](https://github.com/caktus/django-filters-facet/actions/workflows/test.yaml)

A live demo is available on https://facets.caktus-built.com/films/.

For example, the sidebar interface when [searching a library's
catalog](https://durhamcounty.bibliocommons.com/v2/search?query=django&searchType=keyword):

![Example facet screenshot](https://django-filters-facet.s3.amazonaws.com/static/facets-screenshot.png)

## Installation

Install using pip:

```sh
# Until we release on pypi...
pip install git+https://github.com/caktus/django-filters-facet.git@main#egg=django-filters-facet
```

## Usage

django-filters-facet provides a `FacetedFilterSet` class that calls a
`configure_facets()` method that can be used for configuring facets. For
example, if you had a Film model you could have a filterset for it with the
code:

```python
# example-facets/films/filters.py
from django_filters_facet import Facet, FacetedFilterSet

from .models import Film


class FilmFilterSet(FacetedFilterSet):

    class Meta:
        model = Film
        fields = ["type", "release_year", "rating", "listed_in"]

    def configure_facets(self):
        self.filters["type"].facet = Facet()
        self.filters["rating"].facet = Facet()
```

And then in your view, you pass the QuerySet through the `FilmFilterSet` and add
it to the template context:

```python
# example-facets/films/views.py
from django.views.generic.list import ListView

from .filters import FilmFilterSet
from .models import Film


class FilmListView(ListView):

    model = Film

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_set = FilmFilterSet(self.request.GET, queryset=qs)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter_set
        return context
```

And finally, show the facets in your template:

```html
{% load search_tags %}

<aside>{% show_facets filter %}</aside>
```

## Contributing

If you think you've found a bug or are interested in contributing to
this project, check out [django-filters-facet on Github](https://github.com/caktus/django-filters-facet).

Development sponsored by [Caktus Consulting Group, LLC](http://www.caktusgroup.com/).

### Example project

See `example-facets/README.md` documents how to setup the app,
`django_filters_facet`, and the `example-facets` Django project for development.

### Unit tests

Run tests:

```sh
poetry run pytest --cov-report=html
```

import logging

from django.db.models import Count

logger = logging.getLogger(__name__)


class Facet:
    """
    A facet is added to a filter to provide a count of results that
    share values within that filter's field.
    """

    def __init__(self, exclude=None, queryset=None, group_by_filter_name=False):
        self.exclude = exclude
        self.queryset = queryset
        self.group_by_filter_name = group_by_filter_name

    @property
    def filter_name(self):
        """The filter's attribute name on the FilterSet class."""
        return self.filter.filter_field_name

    @property
    def group_by(self):
        """
        Return group by value to count facet items. Defaults to the Filter's
        field_name, but can be overridden to use the Filter's name.
        """
        return self.filter_name if self.group_by_filter_name else self.filter.field_name

    @property
    def form(self):
        """The associated filter's Django form."""
        return self.filter.parent.form

    @property
    def form_field(self):
        """The form field for this facet."""
        return self.form.fields[self.filter_name]

    def is_filtered(self):
        """Return True if this Facet is currently filtered and active."""
        if self.filter.parent.is_valid():
            return self.filter_name in self.form.cleaned_data

    def get_filtered_value(self):
        """
        Return the FilterSet field's current filtered (and cleaned) value or, in other
        words, the facet item chosen by the user.
        """
        if self.filter.parent.is_valid():
            return self.form.cleaned_data.get(self.filter_name)

    def get_queryset(self):
        qs = self.filter.parent.qs
        if self.exclude:
            qs = qs.exclude(self.exclude)
        if self.queryset:
            qs = self.queryset(qs)
        return qs

    def get_items(self):
        """
        Return the count of results that share values for this field. By default,
        this is generated by annotating a values() QuerySet, but may be customized
        by passing in items when constructing the Facet.
        """
        qs = self.get_queryset()
        return qs.values(self.group_by).annotate(count=Count("pk")).order_by("-count")

    def get_facet_item_value(self, value):
        """
        Render the raw value for a facet's item as it would be rendered by
        a form widget, e.g. given a model object, return the primary key.
        """
        raw_value = self.form_field.prepare_value(value)
        # To support filtering by None values, set the raw_value to the special
        # None value defined on the ChoiceFilter.
        # https://django-filter.readthedocs.io/en/stable/ref/filters.html?highlight=null_value#choicefilter
        if (
            raw_value is None
            and hasattr(self.form_field, "null_value")
            and self.form_field.null_value
        ):
            raw_value = self.form_field.null_value
        try:
            return int(raw_value)
        except (TypeError, ValueError):
            return raw_value

    def get_facet_item_label(self, item_value):
        """
        Return the human-readable value for a facet's item, which defaults to the
        actual value set on the model unless the field is a ChoiceField.
        """
        if not hasattr(self.form_field, "choices"):
            return item_value
        for value, label in self.form_field.choices:
            if value == item_value:
                return label

    def get_facet_item_is_active(self, item_value, filtered_value):
        """Return True if the facet is currently filtered by this facet item."""
        if self.is_filtered():
            raw_filtered_value = self.get_facet_item_value(filtered_value)
            return raw_filtered_value == item_value
        return False

    def items_for_display(self):
        """Returns context data for displaying the facet's values and counts."""
        logger.debug(self.filter_name)
        filtered_value = self.get_filtered_value()
        facet_item_counts = self.get_items()
        if self.is_filtered() and not facet_item_counts:
            # If this facet is filtered BUT there are no items, then the search reduced
            # the results to zero results. The facet should still show.
            facet_item_counts = [{self.group_by: filtered_value, "count": 0}]
        for item in facet_item_counts:
            item_value = self.get_facet_item_value(item[self.group_by])
            data = {
                "label": self.get_facet_item_label(item_value=item_value),
                "value": item_value,
                "count": item["count"],
                "is_active": self.get_facet_item_is_active(item_value, filtered_value),
            }
            logger.debug(data)
            yield data

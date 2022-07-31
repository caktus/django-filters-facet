from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def add_qsarg(context, name, value):
    query_dict = context["request"].GET.copy()
    if value not in query_dict.getlist(name):
        query_dict.appendlist(name, value)
    if "page" in query_dict:
        query_dict.pop("page")
    return "?" + query_dict.urlencode()


@register.simple_tag(takes_context=True)
def remove_qsarg(context, name):
    query_dict = context["request"].GET.copy()
    if name in query_dict:
        query_dict.pop(name)
    if "page" in query_dict:
        query_dict.pop("page")
    return "?" + query_dict.urlencode()


@register.inclusion_tag("search/facets.html", takes_context=True)
def show_facets(context, filter_):
    return {
        "filter": filter_,
        "request": context["request"],
    }


@register.simple_tag
def get_facet_display(filter_set, filter_name, value):
    facet = filter_set.filters[filter_name].facet
    return facet.get_facet_item_label(value)

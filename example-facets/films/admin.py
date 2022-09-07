from django.contrib import admin

from .models import Film


@admin.register(Film)
class FlimAdmin(admin.ModelAdmin):
    date_hierarchy = "release_year"
    list_display = ("title", "type", "director", "rating", "duration", "release_year")
    list_filter = ("type", "rating", "date_added")
    search_fields = ("title", "id")
    ordering = ("title",)

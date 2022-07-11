from django.db import models


class Stop(models.Model):
    PURPOSE_CHOICES = (
        (1, "Speed Limit Violation"),
        (2, "Stop Light/Sign Violation"),
        (3, "Driving While Impaired"),
        (4, "Safe Movement Violation"),
        (5, "Vehicle Equipment Violation"),
        (6, "Vehicle Regulatory Violation"),
        (7, "Seat Belt Violation"),
        (8, "Investigation"),
        (9, "Other Motor Vehicle Violation"),
        (10, "Checkpoint"),
    )

    SEARCH_TYPE_CHOICES = (
        (1, "Consent"),
        (2, "Search Warrant"),
        (3, "Probable Cause"),
        (4, "Search Incident to Arrest"),
        (5, "Protective Frisk"),
    )

    RACE_CHOICES = (
        ("A", "Asian"),
        ("B", "Black"),
        ("H", "Hispanic"),
        ("I", "Native American"),
        ("U", "Other"),
        ("W", "White"),
    )

    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))

    date = models.DateTimeField()
    stop_purpose = models.PositiveSmallIntegerField(choices=PURPOSE_CHOICES)
    engage_force = models.BooleanField()
    search_type = models.PositiveSmallIntegerField(
        choices=SEARCH_TYPE_CHOICES, null=True, blank=True
    )
    contraband_found = models.BooleanField()
    officer_id = models.CharField(max_length=15)
    driver_race = models.CharField(max_length=2, choices=RACE_CHOICES)
    driver_gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

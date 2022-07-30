from django.db import models

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

ACTION_CHOICES = (
    (1, "Verbal Warning"),
    (2, "Written Warning"),
    (3, "Citation Issued"),
    (4, "On-View Arrest"),
    (5, "No Action Taken"),
)


PERSON_TYPE_CHOICES = (("D", "Driver"), ("P", "Passenger"))


GENDER_CHOICES = (("M", "Male"), ("F", "Female"))


ETHNICITY_CHOICES = (("H", "Hispanic"), ("N", "Non-Hispanic"))


RACE_CHOICES = (
    ("A", "Asian"),
    ("B", "Black"),
    ("I", "Native American"),
    ("U", "Other"),
    ("W", "White"),
)

SEARCH_TYPE_CHOICES = (
    (1, "Consent"),
    (2, "Search Warrant"),
    (3, "Probable Cause"),
    (4, "Search Incident to Arrest"),
    (5, "Protective Frisk"),
)


SEARCH_BASIS_CHOICES = (
    ("ER", "Erratic/Suspicious Behavior"),
    ("OB", "Observation of Suspected Contraband"),
    ("OI", "Other Official Information"),
    ("SM", "Suspicious Movement"),
    ("TIP", "Informant Tip"),
    ("WTNS", "Witness Observation"),
)


class Stop(models.Model):
    stop_id = models.PositiveIntegerField(primary_key=True)
    agency_description = models.CharField(max_length=100)
    agency = models.ForeignKey(
        "Agency", null=True, related_name="stops", on_delete=models.CASCADE
    )
    date = models.DateTimeField(db_index=True)
    purpose = models.PositiveSmallIntegerField(choices=PURPOSE_CHOICES)
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)
    driver_arrest = models.BooleanField(default=False)
    passenger_arrest = models.BooleanField(default=False)
    encounter_force = models.BooleanField(default=False)
    engage_force = models.BooleanField(default=False)
    officer_injury = models.BooleanField(default=False)
    driver_injury = models.BooleanField(default=False)
    passenger_injury = models.BooleanField(default=False)
    officer_id = models.CharField(max_length=15)  # todo: keys
    stop_location = models.CharField(max_length=15)  # todo: keys
    stop_city = models.CharField(max_length=20)


class Person(models.Model):
    class Race(models.TextChoices):
        ASIAN = "A", "Asian"
        BLACK = "B", "Black"
        NATVE_AMERICAN = "I", "Native American"
        OTHER = "U", "Other"
        WHITE = "W", "White"
        HISPANIC = "H", "Hispanic"

    class Ethnicity(models.TextChoices):
        HISPANIC = "H", "Hispanic"
        NON_HISPANIC = "N", "Non-Hispanic"

    person_id = models.IntegerField(primary_key=True)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=PERSON_TYPE_CHOICES)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    ethnicity = models.CharField(max_length=2, choices=Ethnicity.choices)
    race = models.CharField(max_length=2, choices=Race.choices)


class Search(models.Model):
    search_id = models.IntegerField(primary_key=True)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.PositiveSmallIntegerField(choices=SEARCH_TYPE_CHOICES)
    vehicle_search = models.BooleanField(default=False)
    driver_search = models.BooleanField(default=False)
    passenger_search = models.BooleanField(default=False)
    property_search = models.BooleanField(default=False)
    vehicle_siezed = models.BooleanField(default=False)
    personal_property_siezed = models.BooleanField(default=False)
    other_property_sized = models.BooleanField(default=False)


class Contraband(models.Model):
    contraband_id = models.IntegerField(primary_key=True)
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    ounces = models.FloatField(default=0, null=True)
    pounds = models.FloatField(default=0, null=True)
    pints = models.FloatField(default=0, null=True)
    gallons = models.FloatField(default=0, null=True)
    dosages = models.FloatField(default=0, null=True)
    grams = models.FloatField(default=0, null=True)
    kilos = models.FloatField(default=0, null=True)
    money = models.FloatField(default=0, null=True)
    weapons = models.FloatField(default=0, null=True)
    dollar_amount = models.FloatField(default=0, null=True)


class SearchBasis(models.Model):
    search_basis_id = models.IntegerField(primary_key=True)
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    basis = models.CharField(max_length=4, choices=SEARCH_BASIS_CHOICES)


class Agency(models.Model):
    name = models.CharField(max_length=255)
    census_profile_id = models.CharField(max_length=16, blank=True, default="")
    last_reported_stop = models.DateField(null=True)

    class Meta(object):
        verbose_name_plural = "Agencies"

    def __str__(self):
        return self.name

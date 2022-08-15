from django.db import models


class Statute(models.Model):
    title = models.CharField(max_length=2048)
    summary = models.TextField()
    date = models.DateField(null=True)
    subjects = models.ManyToManyField("Subject", related_name="statutes")
    jurisdictions = models.ManyToManyField("Jurisdiction", related_name="statutes")
    related_dates = models.ManyToManyField("Date", related_name="statutes")

    def __str__(self) -> str:
        return self.title


class Subject(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name


class Jurisdiction(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name


class Date(models.Model):
    date = models.DateField()

    def __str__(self) -> str:
        return self.date

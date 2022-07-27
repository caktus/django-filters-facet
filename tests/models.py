from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)


class Student(models.Model):
    class Grade(models.IntegerChoices):
        PREK = -1, "Pre-K"
        KINDERGARTEN = 0, "K"
        FIRST = 1, "1st"
        SECOND = 2, "2nd"
        THIRD = 3, "3rd"
        FOURTH = 4, "4th"
        FIFTH = 5, "5th"
        SIXTH = 6, "6th"
        SEVENTH = 7, "7th"
        EIGHTH = 8, "8th"
        NINTH = 9, "9th"
        TENTH = 10, "10th"
        ELEVENTH = 11, "11th"
        TWELTH = 12, "12th"

    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade = models.SmallIntegerField(choices=Grade.choices)
    dob = models.DateField()

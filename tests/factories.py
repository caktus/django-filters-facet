import factory

from .models import School, Student


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = School

    name = factory.Faker("company")


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    name = factory.Faker("name_nonbinary")
    school = factory.SubFactory(SchoolFactory)
    grade = Student.Grade.FIRST

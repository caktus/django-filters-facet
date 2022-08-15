import factory

from .models import Class, School, Student


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
    dob = factory.Faker("date_of_birth")

    @factory.post_generation
    def classes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for class_ in extracted:
                self.classes.add(class_)


class ClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Class

    name = factory.Faker("catch_phrase")

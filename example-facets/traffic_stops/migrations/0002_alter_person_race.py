# Generated by Django 4.0.7 on 2022-08-17 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("traffic_stops", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="race",
            field=models.CharField(
                choices=[
                    ("A", "Asian"),
                    ("B", "Black"),
                    ("I", "Native American"),
                    ("U", "Other"),
                    ("W", "White"),
                    ("H", "Hispanic"),
                ],
                max_length=2,
            ),
        ),
    ]

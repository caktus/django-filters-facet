# Generated by Django 4.0.7 on 2022-08-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0003_alter_film_country_alter_film_duration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="film",
            name="director",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="film",
            name="show_id",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="film",
            name="title",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="film",
            name="type",
            field=models.CharField(max_length=1000),
        ),
    ]
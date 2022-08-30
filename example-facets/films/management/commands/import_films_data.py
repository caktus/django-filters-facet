from django.core import management
from django.core.management.base import BaseCommand
from films.data import load
from films.models import Film


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="/code/films/data/netflix_titles.csv",
            help="Use local JSON file to load data",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            default=False,
            help="Clean films-related models before loading data file",
        )

    def handle(self, *args, **options):
        if options["clean"]:
            self.stdout.write("Deleting existing films data...")
            Film.objects.all().delete()
            management.call_command("migrate", "films", "zero")
            management.call_command("migrate", "films")
        if options["file"]:
            self.stdout.write("Importing from local file...")
        load.run(local_file=options["file"])

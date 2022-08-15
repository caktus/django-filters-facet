from django.core import management
from django.core.management.base import BaseCommand
from firearms.data import load


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--file", default="", help="Use local JSON file instead of S3 URL"
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            default=False,
            help="Clean firearm-related models before loading data file",
        )

    def handle(self, *args, **options):
        if options["clean"]:
            self.stdout.write("Deleting existing firearms data...")
            management.call_command("migrate", "firearms", "zero")
            management.call_command("migrate", "firearms")
        if options["file"]:
            self.stdout.write("Importing from local file...")
        load.run(local_file=options["file"])

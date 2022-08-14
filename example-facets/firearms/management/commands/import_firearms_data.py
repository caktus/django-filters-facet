from django.core.management.base import BaseCommand
from firearms.data import load


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--url", default="")

    def handle(self, *args, **options):
        load.run()

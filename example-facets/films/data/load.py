import json

from datetime import datetime as dt

from pathlib import Path

import requests
import csv

from django.db import transaction
from films.models import Film
from tqdm import tqdm

DEFAULT_URL = "https://django-filters-facet.s3.amazonaws.com/TBD"


def load_data_file(local_file):
    """Download data from S3 or read in local file."""
    if local_file:
        with Path(local_file).open(encoding="UTF-8") as source:
            objects = [row for row in csv.DictReader(source)]
    else:
        r = requests.get(DEFAULT_URL)
        objects = r.json()
    return objects


@transaction.atomic()
def run(local_file=""):
    objects = load_data_file(local_file=local_file)
    for obj in tqdm(objects):
        obj["date_added"] = dt.strptime(str, "%m-%d-%y")
        law = Film.objects.create(**obj)

# (objects.date_added)
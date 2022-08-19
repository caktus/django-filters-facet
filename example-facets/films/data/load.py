import json
import csv

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
        local_date_time = obj["date_added"].strip()
        if not local_date_time:
            continue
        obj["date_added"] = dt.strptime(local_date_time, "%B %d, %Y")
        law = Film.objects.create(**obj)

    print(obj)

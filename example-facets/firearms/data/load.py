import json

from pathlib import Path

import requests

from django.db import transaction
from firearms.models import Date, Jurisdiction, Statute, Subject
from tqdm import tqdm

DEFAULT_URL = "https://django-filters-facet.s3.amazonaws.com/firearms/firearm-laws.json"


def load_data_file(local_file):
    """Download data from S3 or read in local file."""
    if local_file:
        with Path(local_file).open(encoding="UTF-8") as source:
            objects = json.load(source)
    else:
        r = requests.get(DEFAULT_URL)
        objects = r.json()
    return objects


@transaction.atomic()
def run(local_file=""):
    objects = load_data_file(local_file=local_file)
    for obj in tqdm(objects):
        years = obj.get("years", [])
        date = f"{years[0]}-01-01" if years else None
        law = Statute.objects.create(
            title=obj["title"], summary=obj["summary"], date=date
        )
        for name in obj.get("subjects", []):
            subject, _ = Subject.objects.get_or_create(name=name)
            law.subjects.add(subject)
        for name in obj.get("jurisdictions", []):
            jurisdiction, _ = Jurisdiction.objects.get_or_create(name=name)
            law.jurisdictions.add(jurisdiction)
        for year in years:
            date, _ = Date.objects.get_or_create(date=f"{year}-01-01")
            law.related_dates.add(date)

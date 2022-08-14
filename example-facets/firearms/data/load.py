import json

from pathlib import Path

from django.conf import settings
from django.db import transaction
from firearms.models import Date, Jurisdiction, Statute, Subject
from tqdm import tqdm


@transaction.atomic()
def run():
    path = settings.BASE_DIR / "firearms" / "data" / "firearm-laws.json"
    with Path(path).open(encoding="UTF-8") as source:
        objects = json.load(source)
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

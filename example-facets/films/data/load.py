import csv

from datetime import datetime as dt
from pathlib import Path

from django.db import transaction
from films.models import Film, Genre
from tqdm import tqdm


@transaction.atomic()
def run(local_file):
    with Path(local_file).open(encoding="UTF-8") as source:
        objects = [row for row in csv.DictReader(source)]
    for obj in tqdm(objects):
        local_date_time = obj["date_added"].strip()
        local_release_year = obj["release_year"].strip()
        if not local_date_time:
            continue
        obj["date_added"] = dt.strptime(local_date_time, "%B %d, %Y")
        obj["release_year"] = dt.strptime(local_release_year, "%Y")
        film = Film.objects.create(**obj)
        genre_names = [n.strip() for n in obj["listed_in"].split(",")]
        for name in genre_names:
            genre, _ = Genre.objects.get_or_create(name=name)
            film.genres.add(genre)

import json
import logging
import pathlib
import re
import sys

import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)


ROOT_URI = "https://firearmslaw.duke.edu/search-results/"


logger = logging.getLogger("scraper")


def scrape_detail(uri):
    r = requests.get(uri)
    soup = BeautifulSoup(r.content, features="html.parser")
    title = soup.find("h1").text
    logger.info(title)
    summary = soup.select_one("div.row p").text
    soup = soup.select("div.law-info div")
    subjects = [tag.text for tag in soup[0].select("a[rel=tag]")]
    jurisdictions = [tag.text for tag in soup[1].select("a[rel=tag]")]
    year_groups = [
        re.findall("([1-3][0-9]{3})", tag.text) for tag in soup[2].select("a[rel=tag]")
    ]
    years = [item for items in year_groups for item in items]

    detail = {
        "title": title,
        "summary": summary,
        "subjects": subjects,
        "jurisdictions": jurisdictions,
        "years": years,
    }
    return detail


def scrape_list():
    data = []
    r = requests.get(ROOT_URI)
    soup = BeautifulSoup(r.content, features="html.parser")
    anchors = soup.select("div.post-outer h4 a")
    for anchor in tqdm(anchors):
        detail = scrape_detail(anchor.get("href"))
        data.append(detail)
    return data


def main():
    data = scrape_list()
    with pathlib.Path("firearm-laws.json").open("w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()

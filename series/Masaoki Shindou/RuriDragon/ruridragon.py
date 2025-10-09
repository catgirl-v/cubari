#!/usr/bin/env python3

import datetime
import json
import operator
import pathlib
import urllib.parse as urlparse

import bs4
import feedparser

series_dir = pathlib.Path("series/Masaoki Shindou/RuriDragon/")
chapters_file = series_dir / "chapters.json"

def save_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)

def iso8601_to_unix(date):
    return int(datetime.datetime.fromisoformat(date).timestamp())

try:
    with open(chapters_file) as f:
        chapters = json.load(f)
except FileNotFoundError:
    chapters = {}

def iter_feed():
    page = 1
    while True:
        feed = feedparser.parse(f"https://ruridragon.com/feed/atom?paged={page}", sanitize_html=False)
        if not feed.entries:
            break

        for e in feed.entries:
            yield e

        page += 1

for p in iter_feed():
    parsed_id = urlparse.urlparse(p.id)
    id_query = urlparse.parse_qs(parsed_id.query)
    post_id = id_query["p"][0]
    if post_id in chapters:
        break

    b = bs4.BeautifulSoup(p.content[0].value, "lxml")
    images = b.find_all("img")
    urls = [i["src"] for i in images]

    published = iso8601_to_unix(p.published)
    updated = iso8601_to_unix(p.updated)
    chapters[post_id] = {
        "title": p.title,
        "groups": {
            "Shueisha": urls,
        },
        "last_updated": max(published, updated),
    }

chapters = dict(sorted(chapters.items(), key=lambda kv: int(kv[0])))
save_json(chapters, chapters_file)

chapters = {str(n): c for n, (_, c) in enumerate(chapters.items(), start=1)}
cubari = {
    "$schema": "../../../schema/cubari/gistSource.schema.json",
    "title": "RuriDragon",
    "description": "Ruri faces the usual issues: pushy classmates, annoying teachers and...waking up with dragon horns?!",
    "artist": "Masaoki Shindou",
    "author": "Masaoki Shindou",
    "cover": "https://ruridragon.com/wp-content/uploads/2024/02/RuriDragon_Vol1.webp",
    "chapters": chapters,
}

save_json(cubari, series_dir / "cubari.json")

#!/usr/bin/env python3

import datetime
import json
import operator
import pathlib
import urllib.parse as urlparse

import bs4
import feedparser

series_dir = pathlib.Path("series/Xanthippe Hutcheon/Pandora's Tale/")
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
        feed = feedparser.parse(f"https://pandorastale.com/feed/atom?paged={page}", sanitize_html=False)
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
    url = b.img["data-orig-file"]

    published = iso8601_to_unix(p.published)
    updated = iso8601_to_unix(p.updated)
    chapters[post_id] = {
        "title": p.title,
        "groups": {
            "Xan": [url],
        },
        "last_updated": max(published, updated),
    }
    break

save_json(chapters, chapters_file)

chapters = sorted(chapters.items(), key=operator.itemgetter(0))
chapters = {str(n): c for n, (_, c) in enumerate(chapters, start=1)}

cubari = {
    "$schema": "../../../schema/cubari/gistSource.schema.json",
    "title": "Pandora's Tale",
    "description": "\"What am I for?\"\n\nPandora was a girl created to serve. She wasn’t supposed to want more. She wasn’t supposed to think for herself. She wasn’t supposed to fight back.\n\nShe wasn’t supposed to be a girl.",
    "artist": "Xanthippe Hutcheon",
    "author": "Xanthippe Hutcheon",
    "cover": "https://pandorastale.com/wp-content/uploads/2019/10/1-0-1.png",
    "chapters": chapters,
}

save_json(cubari, series_dir / "cubari.json")

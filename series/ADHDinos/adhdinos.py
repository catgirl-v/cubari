#!/usr/bin/env python3

import json
import re

import requests

url = "https://www.adhdinos.com/app/cms/api/v1/instagram/6a009cb0-f892-11ec-802a-3f8c5f149c9a/assets"

entries = []

max_id = None
while True:
    params = {
        "per_page": 128,
        "max_id": max_id,
        "show_hidden": 0,
    }
    response = requests.get(url, params=params).json()

    entries.extend(response["assets"])

    if max_id := response.get("next_max_id") is None:
        break

chapters = {}
hashtag = re.compile(r"#+\w+")
for n, e in enumerate(reversed(entries), start=1):
    title = e["caption"]
    title = hashtag.sub("", title).strip()

    chapters[str(n)] = {
        "title": title,
        "groups": {
            "ADHDinos": [
                e["images"]["standard_resolution"]["url"]
            ],
        },
        "last_updated": e["created_time"],
    }

cubari = {
    "$schema": "../../schema/cubari/gistSource.schema.json",
    "title": "ADHDinos",
    "description": "Hyper-focus passion project",
    "artist": "Ryan Keats",
    "author": "Ryan Keats",
    "cover": "https://www.adhdinos.com/uploads/b/b99aff1c958ec1cc221603a698845af861565547d6d17b41f7c115dd4ff8e789/longnecksitblack_1657040274.png",
    "chapters": chapters,
}

with open("series/ADHDinos/cubari.json", "w") as f:
    json.dump(cubari, f, indent=4)

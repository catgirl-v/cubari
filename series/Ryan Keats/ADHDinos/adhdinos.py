#!/usr/bin/env python3

import json

import requests

url = "https://www.reddit.com/r/ADHDinos/new.json"

entries = []

after = None
while True:
    params = {
        "raw_json": 1,
        "limit": 100,
        "after": after,
    }
    headers = { "User-Agent": "catgirl-v:cubari:v.0.0.69 (by the cg-v gang)" }
    response = requests.get(url, params=params, headers=headers).json()

    entries.extend(response["data"]["children"])

    if (after := response["data"].get("after")) is None:
        break

entries = (e["data"] for e in reversed(entries) if not e["data"]["is_self"])
chapters = {}
for n, e in enumerate(entries, start=1):
    url = e["url"]
    if (secure_media := e.get("secure_media")) is not None:
        if (reddit_video := secure_media.get("reddit_video")) is not None:
            if reddit_video["is_gif"]:
                url = reddit_video["fallback_url"]

    chapters[str(n)] = {
        "title": e["title"],
        "groups": {
            "ADHDinos": [
                url,
            ],
        },
        "last_updated": int(e["created"]),
    }

cubari = {
    "$schema": "../../../schema/cubari/gistSource.schema.json",
    "title": "ADHDinos",
    "description": "Hyper-focus passion project",
    "artist": "Ryan Keats",
    "author": "Ryan Keats",
    # Source: https://styles.redditmedia.com/t5_5g4wwf/styles/communityIcon_wkgsxbyp4z381.jpg
    "cover": "https://i.imgur.com/fChFbgD.jpg",
    "chapters": chapters,
}

with open("series/Ryan Keats/ADHDinos/cubari.json", "w") as f:
    json.dump(cubari, f, indent=4)

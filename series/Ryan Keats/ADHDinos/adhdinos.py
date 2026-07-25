#!/usr/bin/env python3

import json
import os

import requests


session = requests.Session()
session.headers.update({
    "User-Agent": "catgirl-v:cubari:v.0.0.69 (by the cg-v gang)",
})

if loid := os.getenv("REDDIT_LOID"):
    session.cookies["loid"] = loid
else:
    session.get(
        "https://www.reddit.com/",
        params={
            "token": "fuckspezfuckspezfuckspezfuckspezfuckspezfuckspezfuckspezfuckspez",
        },
        headers={
            "Referer": "https://www.reddit.com/",
        },
    )

url = "https://www.reddit.com/r/ADHDinos/new.json"

entries = []

after = None
while True:
    params = {
        "raw_json": 1,
        "limit": 100,
        "after": after,
    }
    response = session.get(url, params=params).json()

    entries.extend(response["data"]["children"])

    if (after := response["data"].get("after")) is None:
        break

entries = (e["data"] for e in reversed(entries) if not e["data"]["is_self"])
chapters = {}
for n, e in enumerate(entries, start=1):
    urls = [e["url"]]
    if (secure_media := e.get("secure_media")) is not None:
        if (reddit_video := secure_media.get("reddit_video")) is not None:
            if reddit_video["is_gif"]:
                urls = [reddit_video["fallback_url"]]

    if e.get("is_gallery"):
        urls = []
        gallery_data = e["gallery_data"]
        media_metadata = e["media_metadata"]
        for i in gallery_data["items"]:
            media = media_metadata[i["media_id"]]
            source = media["s"]
            if gif := source.get("gif"):
                urls.append(gif)
            else:
                urls.append(source["u"])

    chapters[str(n)] = {
        "title": e["title"],
        "groups": {
            "ADHDinos": urls,
        },
        "last_updated": int(e["created"]),
    }

cubari = {
    "$schema": "../../../schema/cubari/gistSource.schema.json",
    "title": "ADHDinos (reddit)",
    "description": "Hyper-focus passion project",
    "artist": "Ryan Keats",
    "author": "Ryan Keats",
    # Source: https://styles.redditmedia.com/t5_5g4wwf/styles/communityIcon_wkgsxbyp4z381.jpg
    "cover": "https://i.imgur.com/fChFbgD.jpg",
    "chapters": chapters,
}

with open("series/Ryan Keats/ADHDinos/cubari.json", "w") as f:
    json.dump(cubari, f, indent=4)

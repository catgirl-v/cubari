#!/usr/bin/env python3

import os
import json

import requests
import requests.auth

reddit_user = os.environ["REDDIT_USER"]
reddit_password = os.environ["REDDIT_PASSWD"]
reddit_app_id = os.environ["REDDIT_ID"]
reddit_app_secret = os.environ["REDDIT_SECRET"]

headers = {
    "User-Agent": "catgirl-v:cubari:v.0.0.69 (by the cg-v gang)",
}

response = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    auth=requests.auth.HTTPBasicAuth(reddit_app_id, reddit_app_secret),
    data={
        "grant_type": "password",
        "username": reddit_user,
        "password": reddit_password,
    },
    headers=headers,
).json()
token = response["access_token"]
headers["Authorization"] = f"bearer {token}"

url = "https://oauth.reddit.com/r/ADHDinos/new.json"

entries = []

after = None
while True:
    params = {
        "raw_json": 1,
        "limit": 100,
        "after": after,
    }
    response = requests.get(url, params=params, headers=headers).json()

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
            urls.append(media["s"]["u"])

    chapters[str(n)] = {
        "title": e["title"],
        "groups": {
            "ADHDinos": urls,
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

#!/usr/bin/env python3

import io
import os
import json
import urllib.parse

import requests

googleapis_key = os.environ["TINYVIEW_GOOGLEAPIS_KEY"]

if refresh_token := os.getenv("TINYVIEW_REFRESH_TOKEN"):
    # Get a new token for an existing account
    response = requests.post(
        "https://securetoken.googleapis.com/v1/token",
        params={
            "key": googleapis_key,
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    ).json()
    id_token = response["id_token"]
else:
    # Register a new anonymous account
    response = requests.post(
        "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser",
        params={
            "key": googleapis_key,
        },
    ).json()
    id_token = response["idToken"]

entries = []
headers = {
    "Authorization": f"bearer {id_token}",
    "Content-Type": "application/json",
}
request_data = {
    "data": {
        "series": "adhdinos",
        "records": 20,
        "onlyUnread": False,
    }
}
while True:
    response = requests.post(
        "https://api.tinyview.com/v1/api/story/comics-list",
        headers=headers,
        data=json.dumps(request_data),
    ).json()
    data = response["result"]["data"]
    if not data:
        break
    entries.extend(data)
    request_data["data"]["startAfter"] = data[-1]["storyID"]

chapters = {}
cdn_url = "https://cdn.tinyview.com"
for n, e in enumerate(reversed(entries), start=1):
    urls = [
        cdn_url + e["image"],
    ]

    index_url = cdn_url + e["action"]
    # It *should* be fine to request these every time since they're on the CDN?
    index = requests.get(index_url).json()["comics"]

    cdn_path = index_url.removesuffix("index.json")
    for p in index["panels"]:
        if image := p.get("image"):
            urls.append(cdn_path + image)

    if authors_note := e.get("comment"): # also index["comments"]
        wrapped = io.StringIO("")
        count = 0
        for word in authors_note.split(" "):
            if count > 25:
                wrapped.write("\n")
                count = 0
            wrapped.write(word)
            wrapped.write(" ")
            count += len(word) + 1
        wrapped.seek(0)

        urls.append({
            "description": authors_note,
            "src": "https://fakeimg.pl/1500x2126/ffffff/000000/?" + urllib.parse.urlencode({
                "font": "noto",
                "font_size": 42,
                "text": wrapped.read().strip(),
            }),
        })

    chapters[str(n)] = {
        "title": e["title"], # also index["title"]
        "groups": {
            "ADHDinos": urls,
        },
        "last_updated": int(e["createdAt"] / 1000), # also index["datetime"] (ISO 8601)
    }

cubari = {
    "$schema": "../../../schema/cubari/gistSource.schema.json",
    "title": "ADHDinos (Tinyview)",
    "description": "ADHDinos is a webcomic following Dino the Brontosaurus and his misadventures in mental health.",
    "artist": "Ryan Keats",
    "author": "Ryan Keats",
    # Source: https://styles.redditmedia.com/t5_5g4wwf/styles/communityIcon_wkgsxbyp4z381.jpg
    "cover": "https://i.imgur.com/fChFbgD.jpg",
    "chapters": chapters,
}

with open("series/Ryan Keats/ADHDinos_tinyview/cubari.json", "w") as f:
    json.dump(cubari, f, indent=4)

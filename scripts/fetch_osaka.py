#!/usr/bin/env python3
"""Fotoshi STAC API から大阪エリアの写真を取得し data/osaka.geojson に保存する。

使い方:
    export FOTOSHI_STAC_API_KEY=fshi_xxx
    python3 scripts/fetch_osaka.py
"""
import json
import os
import sys
import time
import urllib.request
from urllib.parse import urlencode

API = "https://api.fotoshi.com/v1/stac/search"
BBOX = "135.3,34.5,135.7,34.8"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "osaka.geojson")
KEEP_ASSETS = ("thumbnail", "image-640", "image-1280", "image-2560")

key = os.environ.get("FOTOSHI_STAC_API_KEY")
if not key:
    sys.exit("FOTOSHI_STAC_API_KEY を設定してください")

url = API + "?" + urlencode({"collections": "fotoshi-photos", "bbox": BBOX, "limit": 100})
features = []
while url:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "User-Agent": "fotoshi-osaka-map"})
    with urllib.request.urlopen(req, timeout=30) as res:
        page = json.load(res)
    for f in page["features"]:
        features.append({
            "type": "Feature",
            "id": f["id"],
            "geometry": f["geometry"],
            "properties": {
                **{k: f["properties"].get(k) for k in ("datetime", "username", "creator_name", "source_organization", "license", "width", "height")},
                "assets": {k: f["assets"][k]["href"] for k in KEEP_ASSETS if k in f["assets"]},
            },
        })
    url = next((l["href"] for l in page.get("links", []) if l["rel"] == "next"), None)
    print(f"{len(features)} / {page.get('numberMatched')}", file=sys.stderr)
    time.sleep(2.5)

features.sort(key=lambda f: f["properties"]["datetime"] or "", reverse=True)
with open(OUT, "w", encoding="utf-8") as fp:
    json.dump({
        "type": "FeatureCollection",
        "bbox": [float(v) for v in BBOX.split(",")],
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": API,
        "features": features,
    }, fp, ensure_ascii=False, separators=(",", ":"))
print(f"saved {len(features)} features -> {OUT}", file=sys.stderr)

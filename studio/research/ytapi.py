#!/usr/bin/env python3
"""YouTube Data API v3 helpers (key injected by the environment's network secret;
never stored in code). Quota: search.list = 100 units, videos.list = 1 unit/50 ids.

Usage:
  python ytapi.py enrich OUT_DIR            # add stats/dates to master.json
  python ytapi.py search OUT_DIR            # gap-filling searches -> api_candidates.json
"""
import json, sys, pathlib, re, urllib.request, urllib.parse, time

API = "https://www.googleapis.com/youtube/v3/"

def call(endpoint, **params):
    url = API + endpoint + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

def iso_dur(s):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else None

def videos(ids):
    out = {}
    for i in range(0, len(ids), 50):
        d = call("videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50]), maxResults=50)
        for v in d.get("items", []):
            s, st = v["snippet"], v.get("statistics", {})
            out[v["id"]] = {"published": s.get("publishedAt"), "channel": s.get("channelTitle"), "channel_id": s.get("channelId"),
                            "title": s.get("title"), "tags": s.get("tags", [])[:10],
                            "audio_lang": s.get("defaultAudioLanguage") or s.get("defaultLanguage"),
                            "duration_s": iso_dur(v["contentDetails"].get("duration")),
                            "views": int(st.get("viewCount", 0)), "likes": int(st["likeCount"]) if "likeCount" in st else None,
                            "comments": int(st["commentCount"]) if "commentCount" in st else None}
    return out

GAP_QUERIES = {
    "02_Garba_Dandiya_Navratri": ["garba reel", "navratri garba look", "garba night vlog", "dandiya night", "navratri grwm",
                                  "garba transition", "ગરબા", "navratri 2026 garba girl", "garba dance girl shorts", "navratri outfit garba"],
    "03_Concerts_Events": ["concert vlog india", "concert grwm", "coldplay concert india vlog", "diljit concert vlog",
                           "arijit singh concert vlog", "aditya gadhvi live", "falguni pathak navratri live", "music festival vlog india",
                           "wedding guest vlog", "event vlog girl"],
    "04_Lifestyle_Vlogging": ["day in my life india girl", "mini vlog india aesthetic", "ahmedabad vlog", "weekend vlog girl india",
                              "gujarati vlog", "travel vlog girl india shorts"],
    "05_Gujarati_Creator_Aesthetics": ["chaniya choli styling", "lehenga transition", "saree transition reel", "ethnic outfit ideas reel",
                                       "festive outfit transition"],
    "01_Gujarati_Dance": ["gujarati song dance reel", "garba dance cover girl"],
}

def main(cmd, out):
    out = pathlib.Path(out)
    if cmd == "enrich":
        rows = json.loads((out / "master.json").read_text())
        meta = videos([r["url"].rsplit("/", 1)[1] for r in rows])
        for r in rows:
            m = meta.get(r["url"].rsplit("/", 1)[1])
            if m:
                r.update({"published": m["published"], "views": m["views"], "likes": m["likes"], "comments": m["comments"],
                          "duration_s": m["duration_s"], "audio_lang": m["audio_lang"], "tags": m["tags"],
                          "creator": m["channel"], "stats_captured": time.strftime("%Y-%m-%d")})
        (out / "master.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
        print("enriched", sum(1 for r in rows if r.get("published")), "of", len(rows))
    elif cmd == "search":
        seen = {r["url"].rsplit("/", 1)[1] for r in json.loads((out / "master.json").read_text())}
        found = []
        for cat, qs in GAP_QUERIES.items():
            for q in qs:
                d = call("search", part="snippet", q=q, type="video", videoDuration="short", regionCode="IN",
                         relevanceLanguage="hi", maxResults=50, order="viewCount", publishedAfter="2024-01-01T00:00:00Z")
                for it in d.get("items", []):
                    vid = it["id"]["videoId"]
                    if vid in seen: continue
                    seen.add(vid); found.append({"id": vid, "category": cat, "query": q})
        meta = videos([f["id"] for f in found])
        for f in found: f.update(meta.get(f["id"], {}))
        (out / "api_candidates.json").write_text(json.dumps(found, ensure_ascii=False, indent=1))
        print("api candidates", len(found))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

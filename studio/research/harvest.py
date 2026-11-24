#!/usr/bin/env python3
"""Reference harvester (Phase 4, batch 1).

Discovery uses only public YouTube search/channel listings (yt-dlp flat mode,
no video download, no sign-in, no bot-check bypass). Visual sampling uses
public thumbnails (frame0 = first frame, hq1-3 = ~25/50/75%, maxres = cover).

Usage: python harvest.py OUT_DIR
"""
import json, subprocess, sys, time, pathlib, re

YTDLP = str(pathlib.Path(__file__).resolve().parents[1] / ".venv/bin/yt-dlp")

CATEGORIES = {
    "01_Gujarati_Dance": [
        "gujarati song dance reel shorts", "gujarati girl dance shorts trending",
        "gujarati dance cover shorts", "gujju girl dance reel", "gujarati wedding dance shorts",
        "dhol dance gujarati shorts girl",
    ],
    "02_Garba_Dandiya_Navratri": [
        "garba reel shorts 2026", "navratri garba girl shorts", "dandiya raas shorts",
        "navratri outfit garba look shorts", "garba cinematic shorts", "navratri vlog shorts gujarati",
    ],
    "03_Concerts_Events": [
        "concert vlog shorts india girl", "coldplay ahmedabad concert shorts", "diljit dosanjh concert vlog shorts",
        "arijit singh concert vlog shorts", "aditya gadhvi live concert shorts", "concert outfit grwm shorts india",
        "sunburn festival vlog shorts", "lollapalooza india vlog shorts", "garba night event vlog shorts", "falguni pathak concert shorts", "kinjal dave live garba shorts",
        "music festival vlog shorts india", "concert night cinematic shorts", "event highlight reel shorts gujarat",
    ],
    "04_Lifestyle_Vlogging": [
        "gujarati vlog shorts girl", "day in my life shorts india girl", "ahmedabad vlog shorts",
        "surat vlog shorts", "gujju girl life shorts", "aesthetic vlog shorts india",
        "mini vlog shorts india girl aesthetic", "weekend vlog shorts mumbai girl", "cafe hopping ahmedabad shorts",
        "friends trip vlog shorts india girls", "travel reel cinematic shorts india girl", "birthday vlog shorts india girl",
    ],
    "05_Gujarati_Creator_Aesthetics": [
        "gujarati outfit transition shorts", "chaniya choli styling shorts", "saree transition reel shorts",
        "festive look grwm shorts india", "gujarati wedding outfit shorts", "ethnic outfit ideas shorts gujarati",
    ],
}

# Vertical Shorts feeds (hashtag pages return 9:16 Shorts only).
HASHTAGS = {
    "01_Gujarati_Dance": ["gujaratidance", "gujaratisong", "gujjugirl", "sangeetdance", "dancereels"],
    "02_Garba_Dandiya_Navratri": ["garba", "navratri", "dandiya", "garbalovers", "navratrilook"],
    "03_Concerts_Events": ["concertvlog", "concert", "aadityagadhvi", "falgunipathak", "diljitdosanjh"],
    "04_Lifestyle_Vlogging": ["minivlog", "dayinmylife", "ahmedabad", "gujaratvlog"],
    "05_Gujarati_Creator_Aesthetics": ["chaniyacholi", "grwm", "outfittransition", "ethnicwear"],
}

# Creator-anchored discovery (shorts tabs). Confirmed anchor first.
CHANNELS = {
    "@rxjvee": ("05_Gujarati_Creator_Aesthetics", "RAJVEE GANDHI"),
    "@Mrunalpanchal": ("04_Lifestyle_Vlogging", "Mrunal Panchal Sharma"),
    "@kritikathatbohogirl": ("05_Gujarati_Creator_Aesthetics", "Kritika Khurana"),
    "@komalpandey3894": ("05_Gujarati_Creator_Aesthetics", "Komal Pandey"),
    "@MasoomMinawala": ("04_Lifestyle_Vlogging", "Masoom Minawala"),
    "@Aashna.Shroff": ("04_Lifestyle_Vlogging", "Aashna Shroff"),
    "@dollysinghofficial": ("04_Lifestyle_Vlogging", "Dolly Singh"),
}

EXCLUDE = re.compile(r"(compilation|status|whatsapp|tik ?tok|#?viral video|full song|lyrics|jukebox|non ?stop|audio|bluey|kids|baby girl|with names?|designs?\b|collection|saas|bahu|official trailer|ost\b)", re.I)


def ytdlp_flat(url, n):
    cmd = [YTDLP, "--flat-playlist", "-J", "--playlist-end", str(n), url]
    for attempt in range(3):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout).get("entries") or []
        time.sleep(3 * (attempt + 1))
    print("WARN failed:", url, r.stderr[-200:], file=sys.stderr)
    return []


def main(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    prev = out / "candidates.json"
    rows = json.loads(prev.read_text()) if prev.exists() else []
    rows = [r for r in rows if not EXCLUDE.search(r["title"]) and not r["discovered_via"].startswith("channel @sanskari")]
    seen = {r["id"] for r in rows}
    def add(e, cat, source, chan=None):
        vid = e.get("id")
        if not vid or vid in seen:
            return
        title = e.get("title") or ""
        dur = e.get("duration")
        if EXCLUDE.search(title):
            return
        if dur is not None and dur > 180:   # reels/shorts focus
            return
        seen.add(vid)
        rows.append({
            "id": vid, "url": f"https://www.youtube.com/shorts/{vid}", "platform": "YouTube Shorts",
            "title": title, "channel": e.get("channel") or e.get("uploader") or chan,
            "channel_id": e.get("channel_id"), "category": cat, "discovered_via": source,
            "duration_s": dur, "views": e.get("view_count"),
            "captured_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
    for r in rows:
        for h, (c, name) in CHANNELS.items():
            if r["discovered_via"] == f"channel {h}" and not r.get("channel"):
                r["channel"] = name
    for handle, (cat, name) in CHANNELS.items():
        for e in ytdlp_flat(f"https://www.youtube.com/{handle}/shorts", 40):
            add(e, cat, f"channel {handle}", name)
    for cat, tags in HASHTAGS.items():
        for t in tags:
            for e in ytdlp_flat(f"https://www.youtube.com/hashtag/{t}/shorts", 50):
                add(e, cat, f"hashtag #{t}")
    for cat, qs in CATEGORIES.items():
        for q in qs:
            for e in ytdlp_flat(f"ytsearch20:{q}", 20):
                add(e, cat, f"search: {q}")
    (out / "candidates.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    by = {}
    for r in rows: by[r["category"]] = by.get(r["category"], 0) + 1
    print(len(rows), "candidates", by)


if __name__ == "__main__":
    main(sys.argv[1])

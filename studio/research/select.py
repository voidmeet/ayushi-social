#!/usr/bin/env python3
"""Select ~200 references (target ~40/category) from candidates.json with transparent rules.

Rules:
 1. Drop titles matching harvest.EXCLUDE or OFF_BRIEF, blocked label/brand/kids channels, MANUAL_EXCLUDE ids.
 2. Popularity floor: hashtag feed >= 50k views, search >= 10k; curated creator channels always eligible.
 3. Enrich via public YouTube oEmbed (author name/url, embed width/height -> orientation).
 4. Prefer 9:16 (we make Reels); horizontal only fills gaps. Max 5 refs per creator per category, 8 overall.
"""
import json, re, sys, pathlib, importlib.util, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("h", here / "harvest.py"); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

BLOCK_CHANNELS = re.compile(r"(saregama|zee music|sun tv|netflix|kalyan|taneira|weverse|incredible india|philharmoni|t-series|tips official|sony music|bluey|daily trending|trending reels|wedmegood|malabar)", re.I)
OFF_BRIEF = re.compile(r"(automobile|tractor|jcb|khedut|status|motivat|full video song|edit'?s\b|anti-?gravity|boliyan|learn how|\bdj\b|dagla|trader|ટ્રેક્ટર|petrol|love song|shayari|attitude|bhakti|bhajan|meldi|maa\b|mataji|comedy|funny|prank|\bbro\b|mom entered|tuition|school|cricket|ipl|news|politic|modi|ai video|how to create|tutorial|recipe|food review|unboxing|skincare routine|hair mask)", re.I)
# Manual curation after review (2026-11-24): off-brief, kids, catalog slideshows, fan-cams, reuploads, non-creator.
MANUAL_EXCLUDE = set("""zBn5I8Di-v8 ftzGgM40Z_Y gADX8RLh4jY FTeoHRdCT3s Unh6cwpgdqQ ibKenCPv2DY O2F0lTmh7R8 OJmxZgPUDGA 4Y30WSQEcHA
ZP5CiwLl0aE inUMnsS8Pz8 R4tAr8r5zac pi6qEOJ3Dww eeaEaQpmevk NeX8N-vawBQ WzVsJe0H-h4 kEvPdp7ism4 hjcj3Pp_orY IG-whsodaqw
QoEOzF1g0Yo YvG7bZnWrbI lMM1VUEoyJE gZpEy3ETT6c XuZ_DFkMdLE jWNQ3fhNsnU fkOJsNXSZcQ 0Vx_5t-8akI cQTZ2CIgJ3I 9accsI_elyk
73t9byJKuhI 6nfwxDdr__Y xMqlRD5sqt0 ysynaVNKr0I sewA0ZdecWY R9lv0eT5k70 7XAh4YlFVTg KqMCDGdyQ0s 7S2UhZcbCHI""".split())


def oembed(r):
    u = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={r['id']}")
    try:
        with urllib.request.urlopen(u, timeout=20) as resp:
            d = json.load(resp)
        r["channel"] = r.get("channel") or d.get("author_name")
        r["channel_url"] = d.get("author_url")
        r["embed_wh"] = [d.get("width"), d.get("height")]
        r["title"] = r["title"] or d.get("title") or ""
    except Exception as e:
        r["oembed_error"] = str(e)[:80]
    return r


def main(out):
    out = pathlib.Path(out); rows = json.loads((out / "candidates.json").read_text())
    pool = []
    for r in rows:
        t = r.get("title") or ""
        if r["id"] in MANUAL_EXCLUDE or h.EXCLUDE.search(t) or OFF_BRIEF.search(t) or BLOCK_CHANNELS.search(r.get("channel") or ""):
            continue
        src = r["discovered_via"]; v = r.get("views") or 0
        if src.startswith("hashtag") and v < 50000: continue
        if src.startswith("search") and v < 10000: continue
        pool.append(r)
    with ThreadPoolExecutor(8) as ex:
        pool = list(ex.map(oembed, pool))
    pool = [r for r in pool if "oembed_error" not in r and not BLOCK_CHANNELS.search(r.get("channel") or "") and not OFF_BRIEF.search(r.get("title") or "")]
    fspec = importlib.util.spec_from_file_location("f", here / "frames.py"); f = importlib.util.module_from_spec(fspec); fspec.loader.exec_module(f)
    import cv2
    fd = out / "frames"; fd.mkdir(exist_ok=True)
    def orient(r):
        p = fd / f"{r['id']}_hq2.jpg"
        im = cv2.imread(str(p)) if f.fetch(f"https://i.ytimg.com/vi/{r['id']}/hq2.jpg", p) else None
        r["orientation_hint"] = "vertical" if (im is not None and f.is_vertical(im)) else "horizontal"
        return r
    with ThreadPoolExecutor(8) as ex:
        pool = list(ex.map(orient, pool))
    sel, per_chan = [], {}
    for cat in h.CATEGORIES:
        cand = sorted([r for r in pool if r["category"] == cat],
                      key=lambda r: (r["orientation_hint"] != "vertical", not r["discovered_via"].startswith("channel"), -(r.get("views") or 0)))
        n, per_cat_chan = 0, {}
        for r in cand:
            c = r.get("channel") or "?"
            if per_cat_chan.get(c, 0) >= 4 or per_chan.get(c, 0) >= 6:
                continue
            per_cat_chan[c] = per_cat_chan.get(c, 0) + 1; per_chan[c] = per_chan.get(c, 0) + 1
            sel.append(r); n += 1
            if n >= 40: break
        print(cat, n, "vertical:", sum(1 for r in sel if r["category"] == cat and r["orientation_hint"] == "vertical"))
    (out / "selected.json").write_text(json.dumps(sel, ensure_ascii=False, indent=1))
    print("pool", len(pool), "selected", len(sel), "creators", len(per_chan))


if __name__ == "__main__":
    main(sys.argv[1])

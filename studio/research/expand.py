#!/usr/bin/env python3
"""Pull Shorts from channels of curated (relevant) references to grow the library."""
import json, sys, pathlib, importlib.util
from concurrent.futures import ThreadPoolExecutor
here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("h", here / "harvest.py"); h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
out = pathlib.Path(sys.argv[1])
chans = json.loads((out / "expand_channels.json").read_text())
cur = json.loads((out / "curated.json").read_text()); seen = {r["id"] for r in cur}
def pull(item):
    url, (cat, name) = item
    return [(e, cat, name, url) for e in h.ytdlp_flat(url.rstrip("/") + "/shorts", 15)]
new = []
with ThreadPoolExecutor(4) as ex:
    for batch in ex.map(pull, chans.items()):
        for e, cat, name, url in batch:
            if e.get("id") in seen: continue
            seen.add(e["id"])
            new.append({"id": e["id"], "url": f"https://www.youtube.com/shorts/{e['id']}", "platform": "YouTube Shorts",
                        "title": e.get("title") or "", "channel": name, "channel_url": url, "category": cat,
                        "discovered_via": f"channel expansion {name}", "duration_s": e.get("duration"), "views": e.get("view_count")})
(out / "expansion.json").write_text(json.dumps(new, ensure_ascii=False, indent=1))
print("new", len(new))

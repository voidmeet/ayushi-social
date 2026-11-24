#!/usr/bin/env python3
"""Fetch public thumbnail frames for selected references, compute simple colour
metrics, and build numbered contact sheets for visual review.

frame0 = first frame (hook/thumbnail), hq1/hq2/hq3 = ~25/50/75% frames.
Usage: python frames.py OUT_DIR
"""
import json, sys, pathlib, subprocess, urllib.request
import numpy as np, cv2

def fetch(url, dest):
    if dest.exists() and dest.stat().st_size > 0:
        return True
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            dest.write_bytes(r.read())
        return True
    except Exception:
        return False

def is_vertical(img):
    """hqN thumbnails are 4:3. A 9:16 video sits in the centre with black or
    blurred side bars; detect via darkness or low sharpness of the side bands."""
    h, w = img.shape[:2]
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cw = int(h * 9 / 16); x0 = (w - cw) // 2
    side = np.hstack([g[:, :x0 - 4], g[:, x0 + cw + 4:]]); centre = g[:, x0:x0 + cw]
    if side.mean() < 12:
        return True
    lap = lambda a: cv2.Laplacian(a, cv2.CV_64F).var()
    return lap(side) < 0.2 * max(lap(centre), 1e-6)

def crop_vertical(img):
    h, w = img.shape[:2]
    if is_vertical(img):
        cw = int(h * 9 / 16); x0 = (w - cw) // 2
        return img[:, x0:x0 + cw]
    return img

def metrics(imgs):
    hsv = [cv2.cvtColor(i, cv2.COLOR_BGR2HSV) for i in imgs]
    lab = [cv2.cvtColor(i, cv2.COLOR_BGR2LAB) for i in imgs]
    return {
        "brightness": round(float(np.mean([h[..., 2].mean() for h in hsv])) / 255, 2),
        "saturation": round(float(np.mean([h[..., 1].mean() for h in hsv])) / 255, 2),
        "warmth": round(float(np.mean([l[..., 2].mean() - 128 for l in lab])), 1),   # +warm / -cool (b*)
        "contrast": round(float(np.mean([cv2.cvtColor(i, cv2.COLOR_BGR2GRAY).std() for i in imgs])) / 128, 2),
        "visual_change": round(float(np.mean([cv2.absdiff(cv2.resize(a, (90, 160)), cv2.resize(b, (90, 160))).mean()
                                              for a, b in zip(imgs, imgs[1:])])) / 255, 2),
    }

def main(out):
    out = pathlib.Path(out); fd = out / "frames"; fd.mkdir(exist_ok=True)
    sel = json.loads((out / "selected.json").read_text())
    tiles = []
    for n, r in enumerate(sel, 1):
        r.setdefault("ref_no", n); n = r["ref_no"]
        imgs = []
        for name in ["frame0", "hq1", "hq2", "hq3"]:
            p = fd / f"{r['id']}_{name}.jpg"
            if fetch(f"https://i.ytimg.com/vi/{r['id']}/{name}.jpg", p):
                im = cv2.imread(str(p))
                if im is not None:
                    imgs.append(cv2.resize(crop_vertical(im), (108, 192)))
        r["frames_available"] = len(imgs)
        hq = [cv2.imread(str(fd / f"{r['id']}_{n}.jpg")) for n in ("hq1", "hq2", "hq3")]
        votes = [is_vertical(i) for i in hq if i is not None]
        r["aspect_ratio"] = "9:16" if votes and sum(votes) * 2 > len(votes) else "horizontal (16:9/4:3)"
        if imgs:
            r["auto_metrics"] = metrics(imgs)
            row = np.hstack(imgs + [np.zeros((192, 108, 3), np.uint8)] * (4 - len(imgs)))
            label = np.full((192, 52, 3), 255, np.uint8)
            cv2.putText(label, str(n), (2, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
            tiles.append(np.hstack([label, row]))
    per = 10
    for s in range(0, len(tiles), per):
        grid = tiles[s:s + per]
        # two columns of refs per sheet
        left = np.vstack(grid[0::2]); right = np.vstack(grid[1::2]) if len(grid) > 1 else np.zeros_like(left)
        if right.shape[0] < left.shape[0]:
            right = np.vstack([right, np.zeros((left.shape[0] - right.shape[0], right.shape[1], 3), np.uint8)])
        cv2.imwrite(str(out / f"sheet_{s // per + 1:02d}.jpg"), np.hstack([left, np.full((left.shape[0], 10, 3), 255, np.uint8), right]),
                    [cv2.IMWRITE_JPEG_QUALITY, 80])
    (out / "selected.json").write_text(json.dumps(sel, ensure_ascii=False, indent=1))
    print("refs", len(sel), "with frames", sum(1 for r in sel if r["frames_available"]), "sheets", -(-len(tiles) // per))

if __name__ == "__main__":
    main(sys.argv[1])

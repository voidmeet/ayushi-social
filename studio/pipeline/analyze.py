#!/usr/bin/env python3
"""Raw footage analyser (Phase 9).

Per clip: ffprobe technicals (honours rotation), loudness/true peak, scene cuts,
motion energy timeline, brightness, face presence, 8 keyframes spread across the
WHOLE clip (never just the start), and speech transcript (faster-whisper, VAD).
Outputs: work/analysis/<clip>.json and a numbered contact sheet per 6 clips.

Usage: python analyze.py MANIFEST OUT_DIR [--no-asr]
"""
import json, sys, subprocess, pathlib, re, numpy as np, cv2

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def probe(p):
    d = json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", p]).stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    rot = 0
    for sd in v.get("side_data_list", []):
        if "rotation" in sd: rot = int(sd["rotation"])
    rot = int(v.get("tags", {}).get("rotate", rot))
    w, h = v.get("width"), v.get("height")
    if abs(rot) in (90, 270): w, h = h, w
    num, den = (v.get("avg_frame_rate") or "0/1").split("/")
    return {"duration": round(float(d["format"]["duration"]), 2), "width": w, "height": h,
            "orientation": "vertical" if h and w and h > w else "horizontal",
            "fps": round(int(num) / max(int(den), 1), 2), "codec": v.get("codec_name"),
            "hdr": v.get("color_transfer") in ("arib-std-b67", "smpte2084"),
            "audio": bool(a), "audio_codec": a and a.get("codec_name")}

def loudness(p):
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", out); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)
    return {"lufs": float(I[-1]) if I else None, "true_peak": float(TP[-1]) if TP else None}

FACE = None  # OpenCV 5 dropped Haar cascades from the main package; face/pose detection to be added via MediaPipe

def visual(p, dur):
    """Sample ~4 fps across the clip at low res (ffmpeg applies rotation)."""
    W, H = 90, 160
    raw = run_bytes(["ffmpeg", "-v", "error", "-i", p, "-vf", f"fps=4,scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2",
                     "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W) if raw else np.zeros((0, H, W), np.uint8)
    if len(fr) < 2: return {"motion_timeline": [], "cuts": [], "brightness": None}
    diff = np.abs(fr[1:].astype(int) - fr[:-1].astype(int)).mean(axis=(1, 2))
    cuts = [round((i + 1) / 4, 2) for i, d in enumerate(diff) if d > max(30, diff.mean() * 4)]
    sec = [float(diff[i:i + 4].mean()) for i in range(0, len(diff), 4)]   # per-second motion
    return {"motion_timeline": [round(x, 1) for x in sec], "motion_mean": round(float(diff.mean()), 2),
            "cuts": cuts, "brightness": round(float(fr.mean()) / 255, 2)}

def run_bytes(cmd):
    return subprocess.run(cmd, capture_output=True).stdout

def keyframes(p, dur, n=8):
    frames, faces = [], 0
    for k in range(n):
        t = dur * (k + 0.5) / n
        b = run_bytes(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1", "-vf", "scale=180:320:force_original_aspect_ratio=decrease,pad=180:320:(ow-iw)/2:(oh-ih)/2", "-f", "image2pipe", "-vcodec", "png", "-"])
        im = cv2.imdecode(np.frombuffer(b, np.uint8), cv2.IMREAD_COLOR) if b else None
        if im is None: im = np.zeros((320, 180, 3), np.uint8)
        cv2.putText(im, f"{t:.0f}s", (4, 314), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        frames.append(im)
    return frames, None

_model = None
def transcribe(p):
    global _model
    from faster_whisper import WhisperModel
    if _model is None: _model = WhisperModel("small", device="cpu", compute_type="int8")
    pcm = run_bytes(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"])
    if not pcm: return {"speech_s": 0, "segments": []}
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, info = _model.transcribe(audio, vad_filter=True, beam_size=1)
    segs = [{"start": round(s.start, 1), "end": round(s.end, 1), "text": s.text.strip(), "no_speech_p": round(s.no_speech_prob, 2)} for s in segs]
    segs = [s for s in segs if s["no_speech_p"] < 0.6 and len(s["text"]) > 1]
    return {"lang_guess": info.language, "lang_p": round(info.language_probability, 2),
            "speech_s": round(sum(s["end"] - s["start"] for s in segs), 1), "segments": segs[:40]}

def main(manifest, out, asr=True):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    m = [r for r in json.load(open(manifest)) if r.get("local")]
    rows = []
    for r in m:
        dst = out / f"{r['clip_id']}.json"
        if dst.exists():
            rows.append(json.loads(dst.read_text())); continue
        p = r["local"]; a = {"clip_id": r["clip_id"], "name": r["name"], "folder": r["folder"], **probe(p)}
        a.update(loudness(p) if a["audio"] else {})
        a.update(visual(p, a["duration"]))
        frames, a["face_ratio"] = keyframes(p, a["duration"])
        cv2.imwrite(str(out / f"{r['clip_id']}_strip.jpg"), np.hstack(frames))
        if asr and a["audio"]: a["speech"] = transcribe(p)
        dst.write_text(json.dumps(a, ensure_ascii=False, indent=1)); rows.append(a)
        print(a["clip_id"], a["duration"], a["orientation"], a["width"], "x", a["height"], a.get("lufs"), "speech", a.get("speech", {}).get("speech_s"), flush=True)
    # contact sheets: 4 clips per sheet, each a labelled strip of 8 frames
    for s in range(0, len(rows), 4):
        strips = []
        for a in rows[s:s + 4]:
            im = cv2.imread(str(out / f"{a['clip_id']}_strip.jpg"))
            lab = np.full((320, 70, 3), 255, np.uint8)
            cv2.putText(lab, a["clip_id"], (2, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)
            strips.append(np.hstack([lab, im]))
        cv2.imwrite(str(out / f"sheet_{s // 4 + 1:02d}.jpg"), np.vstack(strips), [cv2.IMWRITE_JPEG_QUALITY, 78])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--no-asr" not in sys.argv)

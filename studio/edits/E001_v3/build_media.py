#!/usr/bin/env python3
"""E001 v2 media prep: beat-locked shot list → graded 1080x1920 clips (with optical-flow
slow-mo, reverse, speed ramps) + one mastered audio mix (music + SFX peak-aligned).

Timeline anchor: Mixkit "Old Letter" (136 BPM) starts at T0=1.90 s; its drop (music 14.048 s)
lands at T=15.948 s. Beat k (music) = beats[k]; timeline = T0 + beats[k].
"""
import json, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]          # studio/
RAW, SFX, MUS = ROOT / "work/raw", ROOT / "work/sfx", ROOT / "work/music"
OUT = pathlib.Path(__file__).parent / "assets"
B = json.load(open(MUS / "old_letter_beats.json"))
beats, peak = B["beats"], B["sfx_peak"]
T0 = 1.90
T = lambda k: round(T0 + beats[k], 3)

GRADE = ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,"
         "unsharp=5:5:0.55:5:5:0.0,eq=contrast=1.06:saturation=1.10:gamma=0.98,"
         "colorbalance=rs=-0.02:bs=0.05:rh=0.03:bh=-0.02,format=yuv420p")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-600:])

def clip(name, src, start, dur, speed=1.0, reverse=False):
    """Output `dur` seconds of picture. speed<1 = optical-flow slow-mo (minterpolate)."""
    srcdur = dur * speed
    vf = []
    if speed < 1.0:
        vf.append(f"minterpolate=fps={round(30 / speed)}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
        vf.append(f"setpts={1 / speed:.4f}*PTS")
    elif speed > 1.0:
        vf.append(f"setpts={1 / speed:.4f}*PTS")
    if reverse: vf.append("reverse")
    vf += ["fps=30", GRADE]
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-t", f"{srcdur + 0.08:.3f}", "-i", str(RAW / f"{src}.mp4"),
         "-vf", ",".join(vf), "-t", f"{dur + 0.04:.3f}", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "15",
         "-g", "15", str(OUT / "clips" / f"{name}.mp4")])

# ── shot list (name, src, src_in, timeline_start, timeline_end, speed, reverse) ──
SHOTS = [
    ("cold",   "C031", 2.30, 0.00,   1.32,  0.5, False),   # cold open: CO2 jet in slow-mo
    ("rewind", "C031", 0.00, 1.32,   T0,    4.4, True),    # tape rewind back to the morning
    ("i1",     "C019", 0.05, T0,     T(4),  1.0, False),   # ticket + teddy  → "Dear Darshan,"
    ("i2",     "C024", 0.00, T(4),   T(8),  1.0, False),   # wristbands → his letter
    ("i3",     "C020", 0.30, T(8),   T(12), 1.0, False),   # sunset crowd → "so I came."
    ("i4",     "C041", 0.90, T(12),  T(16), 1.0, False),   # dusk, screens
    ("i5",     "C023", 0.00, T(16),  T(19), 1.0, False),   # POV hands in the queue → "with my people"
    ("i6",     "C028", 0.60, T(19),  T(24), 1.0, False),   # Love Letters curtain
    ("i7",     "C037", 0.30, T(24),  T(28), 1.0, False),   # projection, lights go down
    ("b1",     "C030", 0.00, T(28),  T(29), 1.0, False),   # build: one shot per beat
    ("b2",     "C016", 0.50, T(29),  T(30), 1.0, False),
    ("b3",     "C036", 0.00, T(31),  T(32), 1.0, False),   # (beat 30–31 = black + heartbeat)
    ("d1",     "C031", 2.60, T(32),  T(35), 1.0, False),   # DROP: pyro/CO2
    ("d2",     "C036", 2.00, T(35),  T(37), 1.0, False),
    ("d3",     "C016", 1.00, T(37),  T(39), 1.0, False),   # Chapter 1 screen
    ("d4",     "C031", 5.50, T(39),  T(41), 1.0, False),
    ("d5",     "C030", 0.20, T(41),  T(43), 1.0, False),   # Chapter 2: Dard
    ("d6a",    "C036", 5.00, T(43),  T(44), 1.0, False),   # speed ramp: real time…
    ("d6b",    "C036", 5.44, T(44),  T(47), 0.4, False),   # …into slow-mo
    ("whip",   "C031", 8.80, T(47),  T(48), 1.6, False),   # fast blur into the ending
    ("end",    "C031", 11.6, T(48),  T(55), 0.5, False),   # slow-mo climax + sign-off
    ("loop",   "C031", 2.30, T(55),  T(58), 0.5, False),   # rhymes with the cold open → seamless loop
]

def main():
    (OUT / "clips").mkdir(parents=True, exist_ok=True)
    plan = []
    import os
    for name, src, sin, ts, te, sp, rev in SHOTS:
        dur = round(te - ts, 3)
        if not os.environ.get("AUDIO_ONLY"): clip(name, src, sin, dur, sp, rev)
        plan.append({"name": name, "src": src, "src_in": sin, "start": round(ts, 3), "dur": dur, "speed": sp, "reverse": rev})
        print(f"{name:7s} {src} T{ts:6.2f}-{te:6.2f} ({dur:.2f}s) x{sp}{' rev' if rev else ''}")
    END = T(58)
    # ── audio: music (cold-open slice + main), SFX placed so their PEAK lands on the picture ──
    fx = [  # (file, timeline_peak, gain_db, max_len)
        ("impact_trailer", 0.04, -4, 1.4), ("rewind", 1.62, -6, 1.0),
        ("writing", 2.15, -9, 1.2), ("writing", 5.9, -10, 0.9), ("writing", 23.1, -10, 1.2), ("paper_slide", T(4), -9, 1.0),
        ("whoosh_fast2", T(8), -13, 1.0), ("air_woosh", T(16), -14, 1.2),
        ("heartbeat", T(30) + 0.05, -6, 0.9), ("riser", T(32), -7, 2.6),
        ("impact_big", T(32) + 0.03, -3, 3.0), ("crowd_cheer", T(32) + 0.6, -12, 6.0),
        ("zoom_impact", T(37), -9, 1.0), ("whoosh_fast", T(41), -11, 1.2),
        ("swoosh", T(47), -10, 1.4), ("crowd_whistle", T(52), -20, 5.0), ("air_woosh", T(55), -15, 1.2),
    ]
    # v3 music: Mixkit "India" (129.2 BPM) tempo-matched to the 136 BPM grid (atempo 1.0526, pitch kept);
    # its drop onset (30.256 s) lands on the pyro hit at T(32).
    R = 0.46440 / 0.44118
    DROP_SRC = 30.256
    m_start = DROP_SRC - (T(32) - T0) * R          # source second that plays at T0
    cold_src = 33.0                                 # loud post-drop bar for the cold open
    ins = ["-i", str(MUS / "205.mp3"), "-i", str(MUS / "205.mp3")]
    fc = [f"[0:a]atrim={cold_src:.3f}:{cold_src + 1.32 * R:.3f},asetpts=PTS-STARTPTS,atempo={R:.4f},afade=t=out:st=1.18:d=0.14,volume=-1dB[mc]",
          f"[1:a]atrim={m_start:.3f}:{m_start + (END - T0) * R + 0.2:.3f},asetpts=PTS-STARTPTS,atempo={R:.4f},atrim=0:{END - T0:.3f},"
          f"afade=t=in:d=0.08,afade=t=out:st={END - T0 - 0.9:.3f}:d=0.9,adelay={int(T0 * 1000)}|{int(T0 * 1000)}[mm]"]
    labels = ["[mc]", "[mm]"]
    for i, (f, tp, g, ln) in enumerate(fx):
        ins += ["-i", str(SFX / f"{f}.mp3")]
        st = tp - peak[f]
        trim = max(0.0, -st); st = max(0.0, st)
        fc.append(f"[{i + 2}:a]atrim={trim:.3f}:{trim + ln:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(0.05, ln - 0.25):.3f}:d=0.25,"
                  f"volume={g}dB,adelay={int(st * 1000)}|{int(st * 1000)}[f{i}]")
        labels.append(f"[f{i}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,atrim=0:{END:.3f},"
              f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[out]", "-ac", "2", str(OUT / "mix.wav")])
    json.dump({"T0": T0, "end": END, "beats_T": {k: T(k) for k in range(0, 59)}, "shots": plan, "sfx": fx, "cold_music_src": cold_src},
              open(pathlib.Path(__file__).parent / "timeline.json", "w"), indent=1)
    print("END", END, "mix ok")

if __name__ == "__main__":
    main()

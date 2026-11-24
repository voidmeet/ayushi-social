# Stage 1 Smoke Test: 2026-11-24 (Claude Code cloud container)

## Installed (pinned)
| Component | Version | How |
|---|---|---|
| hyperframes (CLI) | 0.9.88 | npm, `--ignore-scripts`, telemetry off (`HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`) |
| ffmpeg-skill | 4.7.1 | npm, `--ignore-scripts` |
| gsap | 3.15.0 | npm, vendored into templates (CDN is blocked here) |
| faster-whisper / scenedetect / librosa / opencv-python-headless | 1.2.1 / 0.7.3 / 1.0.1 / 5.1.0.95 | Python venv; full lock in `studio/requirements.lock.txt` |
| Fonts (OFL) | google/fonts main | Hind Vadodara Regular/SemiBold/Bold, Playfair Display, Mukta Vaani ExtraBold |
| Chromium | preinstalled | `PUPPETEER_EXECUTABLE_PATH=/opt/pw-browsers/chromium` |

## Results
| Test | Result |
|---|---|
| HyperFrames `check` (lint, runtime, layout, contrast) | ✅ passed (warnings: safe-zone on two lines, empty first frame; both fixable) |
| Render 5 s Gujarati card 1080×1920 @30fps H.264 | ✅ 5.000 s, 1080×1920, 30/1, ~11 s render on CPU (software GL) |
| Gujarati shaping, **Hind Vadodara** | ✅ conjuncts correct (કેમ છો?, નવરાત્રી ૨૦૨૬) |
| Gujarati shaping, **Mukta Vaani ExtraBold** | ❌ ત્ર rendered with visible halant (ત્‌ર). **Font rejected** for Gujarati script. |
| Built-in safe-zone check (Reels/Shorts/TikTok) | ✅ available, useful for QC |
| Drive connector binary download | ✅ 2.2 MB MP4 saved straight to disk (no API key needed). Larger files still to test. |
| ffprobe on sample | ✅ H.264 1024×576 with −90° rotation (portrait 576×1024), 30 fps, AAC 44.1k stereo, 10.8 s |
| Black-frame detection | ✅ 0 black segments |
| Loudness (EBU R128) | ✅ measured: −14.0 LUFS integrated, LRA 4.0, **true peak +0.1 dBFS → would clip; needs limiter at −1 dBTP** |
| Scene detection | ✅ 1 scene / 10.8 s, ~530 fps analysis speed |
| faster-whisper transcription | ❌ **BLOCKED**: huggingface.co (model download) refused by session network policy |

## Findings that shape the pipeline
1. Phone clips may be low-resolution (this one is 576 px wide); flag for upscale/quality warning before 1080p export.
2. Honour rotation metadata when probing/cropping.
3. Always apply a true-peak limiter in mastering.
4. First frame must already show the hook (thumbnail rule), enforced by HyperFrames check.

## Blocked / next
- Allow **huggingface.co** (+ its CDN host) in the environment network policy so Whisper models can download, or vendor models another way.
- Test Drive connector with a 100 MB+ MOV.

# Zero-Budget Architecture — Proposal v0.1 (2026-11-24, awaiting approval)

Constraint (user, 2026-11-24): **₹0/month.** Only the existing Claude subscription + open-source tools + free tiers that need no billing account.

## Tested facts this design relies on
| Fact | Tested |
|---|---|
| Claude Code cloud container: 4 vCPU, 15 GB RAM, ~60 GB free disk, FFmpeg/FFprobe, Node 22, Python 3.13, Chromium+Playwright | ✅ 2026-11-24 |
| Google Drive connector reads folder metadata/listings | ✅ |
| googleapis.com reachable from container (auth required) | ✅ |
| instagram.com / youtube.com / drive.google.com web pages blocked by session network | ✅ (blocked) |
| Raw folder is shared "anyone with link: reader" | ✅ (so a free API key can read it, still to test) |

## Components
| Layer | Zero-cost choice | Notes |
|---|---|---|
| Orchestrator + creative brain | **Claude Code cloud sessions** (your subscription) | Runs in Anthropic's cloud, not your PC |
| Autonomy / scheduling | **Claude Code scheduled tasks** (e.g. daily: "check inbox → analyse → plan → render drafts") | Counts against subscription usage limits; not unlimited |
| Media worker | Same cloud container: FFmpeg, faster-whisper (CPU), PySceneDetect, OpenCV, librosa (beats) | No GPU; CPU is fine for this volume |
| Motion graphics / templates | **Remotion or HyperFrames** (decided in Phase 5 audit), headless Chromium | Check licence: Remotion is free for individuals/small teams |
| Fallback heavy renders | GitHub Actions on private repo (2,000 free min/month) | Only if session limits bite |
| Drive read (video download) | **Drive API + free API key** (no billing), saved via secure credential form | Works because folder is link-shared |
| Drive write (reports, scripts, captions) | Drive connector | Small files |
| Drive write (draft MP4s) | Test connector upload size first; fallback: **GitHub Releases in private repo** or OAuth | To be tested |
| Database / queue / history | **SQLite + JSON job manifest, versioned in git** | Idempotent by Drive fileId + md5 |
| Transcription | faster-whisper (open-source) | Gujarati accuracy is moderate; **human check required** |
| Music | Free-licence libraries (e.g. Pixabay Music, YouTube Audio Library) + trending audio added in-app at posting | No paid library |
| Fonts | OFL Gujarati fonts (Hind Vadodara, Mukta Vaani, Noto Gujarati) | Free |
| Review UI | Drive drafts folder + Claude Artifact review page | Free |

## Honest limits
1. Sessions are ephemeral: everything worth keeping goes to git or Drive.
2. Subscription usage limits cap how much autonomous work runs per day/week.
3. No GPU: no heavy AI video models (MotionClone etc.); not needed for premium edits.
4. Whisper Gujarati transcripts need review before captions are burned in.
5. Reference research can't open Instagram/YouTube from the container. Options: you share reel links / screen recordings, or official YouTube Data API (free key).
6. Not 24/7 event-driven; scheduled sync (e.g. daily) instead of instant Drive notifications.

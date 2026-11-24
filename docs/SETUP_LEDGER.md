# Setup Ledger — Gujju Creator Studio
_Last updated: 2026-11-24 · folder ID and other private identifiers intentionally omitted_

## 1. Information provided
- Raw footage parent folder: Google Drive folder link received (Step 1)
- Inspiration: **Rajvee Gandhi (@rxjvee) CONFIRMED** as anchor reference (2026-11-24). Smaller Rajvee-like creators welcome if they fit. "Khushi" still unresolved. Shortlist: docs/research/Creator_Candidate_Shortlist.md
- 15 candidate repos for the Phase 5 audit
- Creator social accounts: **none exist yet** (2026-11-24). Brand name/handle to be decided later.
- Language: **Gujarati + Hinglish mix** (approved 2026-11-24, on Claude's recommendation). Spoken Gujarati is kept as-is, never translated or reworded. On-screen text leans Hinglish with Gujarati words and phrases for identity.
- Caption script (approved 2026-11-24): **body captions in English transliteration**; **Gujarati script only for short "hero" text** (titles, festive lines). Requires a Gujarati-capable font (e.g. Noto Sans/Serif Gujarati, Hind Vadodara, Mukta Vaani; OFL-licensed) and a render test for conjuncts/matras.
- Brand personality (approved "for now", 2026-11-24, revisit after first drafts): **"Warm, playful Gujju girl with effortless style."**
- Aesthetic (approved 2026-11-24): **content-type-adaptive under one identity**. Vlogs = relatable, soft-cinematic, natural tones. Dance/garba/concerts = energetic, cinematic, beat-synced, richer festive colour. Fashion/occasions = elegant/glamorous, clean type, slower polished motion. Fonts, palette and caption style are constant across all.
- Do-not-use list (2026-11-24): **no user-imposed creative restrictions**. Full creative freedom on styles, colours, fonts and effects. Baseline guardrails still apply from the master brief: preserve her natural appearance (no heavy beauty filters or likeness changes without permission), keep her Gujarati meaning intact, use only properly licensed music in exported files, and keep cultural content respectful.
- Consent (2026-11-24): creator **consents** to AI analysis, transcription and editing of her footage and voice (she proposed the project).
- Voiceover: **her own real voice only.** No synthetic or cloned voice and no likeness alteration. Workflow: each edit ships with a timed VO script; she records it; the recording is uploaded and synced into the final edit.
- Platforms (approved 2026-11-24): **Instagram Reels = primary; YouTube Shorts = same edits** with platform-specific safe areas and captions. TikTok excluded (banned in India). Long-form YouTube compilations deferred. Default export 1080×1920 9:16.
- Volume (approved 2026-11-24): **4–5 Reels/week** after launch. Launch backlog target 25–40 edits (estimate; to be confirmed after footage analysis).
- Strategy: content-first. Build a backlog of finished, ready-to-post edits before launch so posting can be regular from day one.

## 2. Connections (tested 2026-11-24)
| Connection | Status | Evidence |
|---|---|---|
| claude.ai Google Drive connector | ✅ Connected (2026-11-24) | Folder metadata, permissions and listings read successfully |
| drive.google.com web page | ❌ Blocked | Session network proxy refuses the host |
| Drive API v3 without credentials | ❌ Denied | googleapis.com returns 403 PERMISSION_DENIED |
| GitHub voidmeet/ayushi-social | ✅ | Empty repo, branch claude/cool-ritchie-x2kj7r |

## 3. Permissions
- Raw footage folder: **READ-ONLY** (link-viewer access; canAddChildren/canEdit/canTrash = false). Folder owned by a different account than the one connected.
- User granted standing permission (2026-11-24) to add plugins/connectors without asking. Anything that bills money still needs approval.

## 3b. Raw folder inventory (2026-11-24, metadata only)
| Subfolder | Files | Size | Types | Upload dates |
|---|---|---|---|---|
| Navratri 2026 | 14 videos | ~0.81 GB | 5 MOV, 9 MP4 | 2026-10-26 |
| Daily Vlog Content | 85 videos | ~10.45 GB | 36 MOV (9.5 GB), 49 MP4 (0.9 GB) | 2026-10-28 → 2026-11-22 |
| **Total** | **99 videos, 0 photos** | **~11.3 GB** | | |
- No nested subfolders. Filenames are device-generated (IMG_####.MOV, UUID.mp4, PXL_…), so names carry no meaning; categories come only from the subfolder.
- Uploaded directly by the creator's own account. Includes at least one already-edited reel ("Aayushi - Reel") and one app export ("video-output-…"). Treat these as finished edits or style references, not raw footage.
- Largest file 2.3 GB (iPhone MOV). Worker must stream to disk, not hold files in memory.
- Incremental automation: suitable. Stable Drive file IDs + modifiedTime + md5Checksum (Drive API) allow detecting changes and duplicates.
## 4. Tools: cloud Linux container, Bash, git/gh, Playwright+Chromium, web research. No Google/IG/YT/TikTok connectors.
## 5. Infrastructure decisions
- FIXED: processing runs in the cloud, never depends on the user's PC
- RECOMMENDED (onboarding): claude.ai Google Drive connector for inspection
- RECOMMENDED (production, Phase 7): dedicated Google Cloud project + OAuth (read-only on source folder; write only to studio folders); secrets in a secrets manager
## 6. Implications recorded
- No own-audience analytics until launch, so early creative decisions rely on the reference research (Phase 4) and the creator's approval.
- Branding (watermark, handle overlays, intro/outro name cards) stays a swappable template variable. Edits must not burn in a name yet.
- Content backlog needs an "evergreen vs time-sensitive" tag (e.g. Navratri 2026 footage dates quickly; best kept for next season or posted as throwback).

## 6b. Missing: all Phase 2–3 info; video-level metadata (duration/fps/resolution) needs ffprobe in the worker
## 7. Awaiting approval / recorded defaults
- DEFAULT: raw folder stays read-only (safest). GUJARATI_CREATOR_STUDIO/ will go in a Drive location we control, decided in Phase 8.
## 8. Completed: [x] Step 1 link received · [x] access check · [x] Phase 2 Creator Profile questions complete → docs/CREATOR_BRAND_PROFILE.md v0.1 · [x] connector connected · [x] folder inspection steps 2–10 (metadata level)

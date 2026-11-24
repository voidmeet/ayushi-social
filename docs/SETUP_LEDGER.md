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
- Length (accepted 2026-11-24): dance/trend 7–15s · garba/Navratri/concerts 15–30s · vlogs/outings/fashion 30–60s · >60s only for special edits.
- Multi-edit (approved 2026-11-24): **yes**, max 2–3 edits per shoot, each with a distinct hook/story/style; space ≥1 week apart in the schedule.
- Publishing (2026-11-24): **user posts manually.** System only suggests day/time per edit in the publish package. Initial default: Mon/Wed/Fri/Sun + 1 flexible trend slot, 7–10 pm IST; refine with analytics after launch. No auto-publishing integration needed for now.
- Events (accepted 2026-11-24): **festival calendar yes**. Next target: Uttarayan (14 Jan 2027). Navratri 2026 footage held for throwback/next season. Long-form compilations deferred until after launch.
- Phase 3 complete. Export profiles: IG Reels 1080×1920 H.264 high, AAC 48kHz, source fps (≤60), loudness ≈ -14 LUFS; YT Shorts same master with Shorts-specific safe areas.
- **Budget: ₹0/month** (2026-11-24). Claude subscription + open-source + no-billing free tiers only. Proposal: docs/ZERO_BUDGET_ARCHITECTURE_PROPOSAL.md (awaiting approval).
- Zero-budget architecture direction: **APPROVED** (2026-11-24). Reference discovery is Claude's job (user instruction).
- Phase 5 audit done (docs/TOOL_AND_SKILL_AUDIT.md): INSTALL HyperFrames + ffmpeg-skill; faster-whisper; ADAPT ghost-editor, Barty-Bart sound-effects, claude-shorts ideas; REJECT MotionClone x2, mattypark (no licence), ychoi-kr, impertio. Not installed yet.
- Stage 1 smoke test (2026-11-24): stack installed (pinned) and render ✅, QC ✅, Drive binary download ✅; Hind Vadodara chosen, Mukta Vaani rejected (ત્ર shaping bug); Whisper ✅ after user-approved network update (Hugging Face + YouTube hosts added to env 'Ayushi<>socials'). See docs/SMOKE_TEST_REPORT.md.
- Studio workspace location (user, 2026-11-24): **inside "Ayushi <> Social media" (owned by meetlearns)**. Connected connector account = cynoimpakt (viewer only there). Recommended least-privilege setup: meetlearns creates an empty `GUJARATI_CREATOR_STUDIO` subfolder and shares ONLY that subfolder with cynoimpakt as Editor, so raw footage stays read-only. Note: files cynoimpakt creates are owned by, and count against, cynoimpakt's 15 GB unless ownership is transferred.
- Drive workspace CREATED (2026-11-24): GUJARATI_CREATOR_STUDIO/ (owned by meetlearns, Editor shared to cynoimpakt) with 00–12 folders, 01_REFERENCE_LIBRARY/01–08 subfolders, and 02_RAW_INBOX/VOICEOVER_RECORDINGS. Folder ID map kept in Drive (00_ADMIN/studio_config.json), not in git. Raw folders remain read-only.
- Known limit: connector uploads go through base64 in tool calls, fine for docs/JSON but impractical for MP4 drafts. Draft video upload path still to be solved (options: Drive API OAuth upload from the worker, or GitHub Releases).
- Phase 4 batch 1 (2026-11-24): 1,354 candidates → 105 screened → **89 verified & analysed** (16 rejected). Gaps: garba 31, concerts 35, lifestyle 21, aesthetics 19, dance 5. Reports v0.1: Editing_Style_Bible, Top_50_Editing_Techniques, Gujarati_Creator_Trend_Report, Reference_Research_Summary (docs/research/). YouTube full metadata blocked by bot check (not bypassed) → propose free YouTube Data API key. Instagram blocked/login-gated → user-shared links.
- YouTube Data API key: user added as env network secret (www.googleapis.com, header X-Goog-Api-Key, path /youtube/v3/). ✅ Tested.
- Phase 4 batch 2: **134 verified references total** (dance 40, garba 20, concerts 16, lifestyle 27, aesthetics 31); gap 66. Master sheet re-uploaded (old one renamed "superseded", not deleted).
- Drive connector **file-reference uploads from disk work** (81 KB CSV ✅). Candidate route for draft MP4s; size limit still to test.
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
## 8. Completed: [x] Step 1 link received · [x] access check · [x] Phase 3 Content & Platform strategy complete · [x] Phase 2 Creator Profile questions complete → docs/CREATOR_BRAND_PROFILE.md v0.1 · [x] connector connected · [x] folder inspection steps 2–10 (metadata level)

# Reference Research Summary: Batches 1–2 (2026-11-24)

## Batch 2 update (YouTube Data API)
- Free YouTube Data API key added (environment network secret, scoped to www.googleapis.com/youtube/v3/; value never seen by Claude).
- All batch-1 rows enriched with **upload date, likes, comments, duration** (105/105).
- 33 targeted gap searches (region IN, ≤90 s, since 2024) → 1,347 candidates → 853 vertical after filters → 50 hand-picked by title → visual review: **45 kept, 5 rejected** (child, off-brief Western/concept content).

| Category | Batch 1 | Batch 2 | **Total verified** | Target | Gap |
|---|---|---|---|---|---|
| 01 Dance | 35 | 5 | **40** | 40 | 0 ✅ |
| 02 Garba / Navratri | 9 | 11 | **20** | 40 | 20 |
| 03 Concerts / Events | 5 | 11 | **16** | 40 | 24 |
| 04 Lifestyle / Vlog | 19 | 8 | **27** | 40 | 13 |
| 05 Aesthetics / Fashion | 21 | 10 | **31** | 40 | 9 |
| **Total** | 89 | 45 | **134** | 200 | **66** |

29 references rated 5/5 fit. New standout techniques from batch 2: ultra-wide low 360 ghagra spin (GCR-114), dandiya-stick transition trigger (GCR-121), garba dupatta hack (GCR-119), GRWM bookend (open on final look, GCR-120), GRWM ending at the venue (GCR-129), star-on-stage + own reaction intercut (GCR-128), ceremony-labelled wedding lookbook (GCR-145), Uttarayan kite-festival vlog (GCR-138).

---
## Batch 1 (original report)

## Honest status
| Metric | Count |
|---|---|
| Target | ~200 analysed references (≈40 per category) |
| Candidates discovered | 1,354 (YouTube search, Shorts hashtag feeds, creator channels) |
| Screened into batch 1 | 105 |
| **Verified & analysed (kept)** | **89** |
| Rejected after visual review | 16 (face-filter comedy, pranks, children, brand ads, vendor craft clips) |
| Rated 5/5 fit for our creator | 20 |
| Rated 4/5 fit | 28 |

**We have 89 verified references, not 200.** Gap: 111.

| Category | Kept | Target | Gap |
|---|---|---|---|
| 01 Gujarati / Indian dance (incl. sangeet) | 35 | 40 | 5 |
| 02 Garba / Dandiya / Navratri | 9 | 40 | **31** |
| 03 Concerts / Events | 5 | 40 | **35** |
| 04 Lifestyle / Vlogging | 19 | 40 | 21 |
| 05 Gujarati creator aesthetics / fashion | 21 | 40 | 19 |

## Method
1. **Discovery:** public YouTube search pages, Shorts hashtag feeds, and Shorts tabs of curated creators (Rajvee Gandhi, Komal Pandey, Kritika Khurana, Mrunal Panchal, Masoom Minawala, Aashna Shroff, Dolly Singh, plus creators surfaced by relevant results). Tool: yt-dlp in *metadata-only* mode. No downloads, no sign-in, no bot-check bypass.
2. **Screening:** title filters (off-brief, kids, catalogues, devotional, memes), popularity floor, creator-diversity caps, manual title review.
3. **Orientation check:** only 9:16 kept. Most "dance" search results were horizontal academy videos and were dropped; hashtag/creator feeds supply true vertical Reels.
4. **Visual analysis:** 4 public thumbnail frames per Short (first frame = hook, ~25/50/75%), reviewed on contact sheets. Each kept reference got hook, typography, grade, camera, structure, lesson and fit score.
5. **Not observable (frames only):** music, SFX, exact cut frequency, caption animation, ending/CTA, likes/comments, upload date. These columns are marked, not guessed.

## Limitations & blockers
- **Instagram is where most Gujarati creators publish**, but instagram.com is blocked in this environment and normally requires login. We do not bypass that. YouTube under-represents garba and concert creators, which explains the two big gaps.
- **Full YouTube metadata** (upload date, likes, comments) is blocked by YouTube's bot check on cloud IPs. Fix: the official **YouTube Data API v3** with a free key (no billing).
- Engagement numbers are view counts captured 2026-11-24 from public listings.

## Next batch plan (to close the 111 gap)
1. Free YouTube Data API key: dates, likes, comments, precise durations, better search filters (region IN, language gu).
2. Targeted creator-channel expansion for garba/Navratri and concert vlogs (Gujarati event pages, concert vloggers).
3. Instagram: user-supplied reel links (fastest), or evaluate the official Instagram Graph API once the creator account exists (only covers our own/business accounts, not competitors).

## Deliverables (this batch)
- Master sheet: `Gujarati_Creator_Reference_Master` (Drive, 01_REFERENCE_LIBRARY) + full CSV in repo
- `Editing_Style_Bible.md` v0.1 · `Top_50_Editing_Techniques.md` v0.1 · `Gujarati_Creator_Trend_Report.md` v0.1

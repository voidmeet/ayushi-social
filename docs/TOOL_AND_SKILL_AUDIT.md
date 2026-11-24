# Tool & Skill Audit (Skills_Audit_Report) — v1, 2026-11-24

**Method:** each repo was shallow-cloned into an isolated scratch directory and read. **No repository code was executed.**
Checks: existence and canonical name, README, SKILL.md, install path, dependencies, license file, last commit, install/network/credential scan (pipe-to-shell, sudo, eval, outbound hosts, API-key usage).
**Constraints applied:** ₹0 budget · runs in the cloud container (4 vCPU, 15 GB RAM, no GPU, Node 22, FFmpeg present) · authenticity (no synthetic likeness) · licensed media only.

## Summary decisions

| # | Repository (canonical) | Purpose | License | Last commit | Decision |
|---|---|---|---|---|---|
| 14 | heygen-com/hyperframes | HTML/CSS/JS → deterministic MP4; agent skills, kinetic captions, catalog blocks | Apache-2.0 | 2026-11-24 | **INSTALL** (primary renderer) |
| 3 | kajisho5/ffmpeg-skill | FFmpeg skill + CLI + MCP with self-verifying outputs (cuts, reframe, loudness, captions, platform exports, QC) | MIT | 2026-11-24 | **INSTALL** (FFmpeg/QC layer) |
| 2 | openai/whisper | Speech recognition | MIT | 2026-08-31 | **ADAPT** → use the same models via **faster-whisper** (≈4× faster on CPU, int8) |
| 5 | kurbaitaev/ghost-editor | Talking-head → finished reel; take selection, face-safe captions, 7 styles, taste profile | MIT | 2026-11-18 | **ADAPT** (borrow face-safe caption placement, style/taste JSON, reference-study prompt; full install only for VO/talking clips) |
| 10 | Barty-Bart/motion-graphics | 6 skills: beat-timed sound effects, SAM 2 object separation, motion B-roll, explainers | MIT | 2026-10-13 | **ADAPT** (`sound-effects`; `object-separation` OPTIONAL for text-behind-subject, slow on CPU) |
| 6 | AgriciDaniel/claude-shorts (brief said "agricidanie") | Long video → shorts: transcript scoring, boundary snapping, Remotion captions | MIT | 2026-04-10 | **ADAPT** ideas (segment scoring, word/silence boundary snapping); don't install (GPU-oriented, Remotion) |
| 7 | cloudai-x/threejs-skills | 13 Three.js knowledge skills | MIT | 2026-10-19 | **OPTIONAL** (only when a 3D effect earns its place) |
| 9 | iart-ai/motion-skills | Index of 19 skill packs (56 skills); upsells iart.ai | MIT | 2026-11-17 | **OPTIONAL** (review `tiktok-video-skills` pack later; ignore paid API) |
| 1 | yt-dlp/yt-dlp | Media/metadata downloader | Unlicense | 2026-11-23 | **OPTIONAL**: metadata only (`--skip-download --dump-json`) for permitted references; never to rip copyrighted reels or music |
| 15 | zhuyansen/awesome-claude-video-skills | Curated list | CC0 | 2026-11-23 | **Reference only** (discovery index; nothing to install) |
| 4 | ychoi-kr/claude-ffmpeg-skill | Basic FFmpeg recipes | MIT | 2025-10-19 | **REJECT** (fully covered by #3; author notes Claude already knows these) |
| 8 | impertio-studio/three.js-claude-skill-package | Three.js skills aimed at AEC/architecture | MIT | 2026-03-30 | **REJECT** (overlaps #7, off-domain) |
| 11 | mattypark/Motion-graphics-skill | Motion director skill | **No license file** (all rights reserved by default) | 2026-10-08 | **REJECT** for code reuse (read for ideas only); also expects ElevenLabs/Pexels/etc. keys |
| 12 | LPengYang/MotionClone | Research: training-free motion transfer for text-to-video | No license file | 2025-06-17 | **REJECT** |
| 13 | Bujiazi/MotionClone | Same code as #12 (co-author's account, identical tree) | No license file | 2025-06-17 | **REJECT** (duplicate) |

## Per-repo notes

### heygen-com/hyperframes: INSTALL
- **Why:** Apache-2.0 (safe for a future multi-creator agency; Remotion needs a paid company licence above small teams). Built for agents, ships Claude Code skills, deterministic headless render, kinetic captions, a block catalogue, and a `/remotion-to-hyperframes` port path. Node ≥22 matches the container. Very active (v0.9.88 of CLI).
- **Cloud:** CLI runs headless in a container; cloud/Lambda render also documented (not needed).
- **Security:** has usage **telemetry**; disable with `HYPERFRAMES_NO_TELEMETRY=1` and `DO_NOT_TRACK=1`. SECURITY.md present. Large monorepo: install the pinned npm CLI, not the whole repo.
- **Limitations:** pre-1.0 (API churn) → pin the exact version; the "Studio app" Pro plan ($25) is **not** needed.

### kajisho5/ffmpeg-skill: INSTALL
- **Why:** contract-based tools (`contract --json`) that state inputs/outputs and **verify the result**, which fits our QC requirements (dimensions, black frames, loudness, safe areas). Also exposes an MCP server. Extremely active; has fuzzing (ClusterFuzzLite) and SECURITY.md.
- **Security:** no pipe-to-shell; `sudo` strings appear only as printed install hints. `ANTHROPIC_API_KEY` appears only in a test that *asserts the tool never calls an LLM*. Good sign.
- **Install:** npm package `ffmpeg-skill@4.7.1` (pin).

### faster-whisper (instead of openai/whisper)
- Same Whisper weights, CTranslate2 backend, int8 on CPU. Plan: `large-v3` or `large-v3-turbo` int8 for Gujarati/Hindi/English with word timestamps. **Gujarati accuracy is moderate; transcripts go through human review before captions are burned in.**

### kurbaitaev/ghost-editor: ADAPT
- Strong ideas: captions that never cover the face, best-take selection, `taste.json` creator taste profile, styles (cinematic, clean, editorial, kinetic, pop…), reference-study prompt.
- Designed for talking-head monologues, not dance/garba. Install is ~4 GB and pulls Mixkit music (free licence) at install time. Optional `GEMINI_API_KEY` features (AI B-roll) are **not** used.

### Barty-Bart/motion-graphics: ADAPT
- `sound-effects`: beat-timed, loudness-measured SFX. Useful for whooshes and hits on transitions.
- Minor code-quality issue: `sound_pass.py` uses Python `eval()` on ffprobe's frame-rate string. Low risk (local tool output) but **patch to `Fraction()`** when adapting.
- `object-separation` (SAM 2) enables "text behind subject". CPU-only is slow; use sparingly on short hero shots.

### MotionClone (#12/#13): REJECT
- Generates *synthetic* video with diffusion models and needs a GPU. That conflicts with the ₹0 budget and the brand rule of authentic footage with no synthetic likeness. No licence file.

## Chosen stack (one tool per job)
| Job | Tool |
|---|---|
| Probe, cut, reframe, loudness, export, QC | FFmpeg/FFprobe via **ffmpeg-skill** |
| Transcription (gu/hi/en, word timings) | **faster-whisper** |
| Scene detection | **PySceneDetect** |
| Beat/onset detection | **librosa** |
| Faces/pose for subject-aware framing & caption placement | **MediaPipe** / OpenCV |
| Motion graphics, kinetic captions, titles, transitions | **HyperFrames** |
| Sound effects timing | adapted **Barty-Bart sound-effects** |
| Caption placement & taste profile concepts | adapted **ghost-editor** |
| Reference metadata (where permitted) | **yt-dlp** metadata mode / YouTube Data API |

## Not yet tested
Nothing above has been installed or run. The next stage is a pinned install in the cloud container plus a smoke test (render a 5 s Gujarati-text card and run one ffprobe QC).

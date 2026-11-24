# E001 QC report — draft v1 (automated + visual, 2026-11-24)
| Check | Result |
|---|---|
| Dimensions / orientation | ✅ 1080×1920, vertical |
| Frame rate | ✅ constant 30/1 |
| Duration | ✅ 24.600 s (matches plan) |
| Black frames (≥0.15 s) | ✅ none |
| Frozen video (≥0.6 s) | ✅ none |
| Audio | ✅ AAC 48 kHz stereo; −14.1 LUFS integrated; true peak −4.5 dBFS; no clipping |
| Text safe zones | ✅ HyperFrames check passed (0 errors); all text in top third, clear of Reels/Shorts UI |
| Text readability | ⚠️ "with my people 🤍" on screen 1.0 s (rule-of-thumb 1.4 s); source clip is only 1.27 s |
| Gujarati/creator speech | n/a: no speech used |
| Watermarks from tools | ✅ none (HyperFrames is open-source, no watermark) |
| Frame-0 hook | ✅ CO₂ jet spectacle + hook text visible at 0.0 s |
| Source quality | ⚠️ sources are 720p phone exports upscaled to 1080p (lanczos + light sharpen); original iPhone MOVs not yet accessible |
| Music rights | ⚠️ live performance audio: replace or duck under in-app licensed track before publishing |
| Not checked | Face-over-text detection (HyperFrames' opencv.js download blocked by network) |

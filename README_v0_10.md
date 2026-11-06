# NHL365 v0.10 – Self-contained Skylines & Logo Order

This is a maintenance release based on NHL365 v0.9. Existing news, matches, English UI, team selection, team colors and three-image rotation are retained.

## Fixes
- All **96 WebP skylines are embedded directly in `index.html`**. The images no longer depend on the `static/skylines/` directory or a working static file route. This is a deliberate tradeoff: the HTML is approximately 1.3 MB before network compression.
- The existing `static/skylines/` directory is also included for standalone asset access and future maintenance.
- Header order: **NHL logo | NHL365 + selected team logo | city skyline | Change Team**.
- Desktop skyline height 64 px; responsive tablet/mobile heights 50/48 px; complete skyline silhouette fits within the image without clipping.
- Header photos remain the three per-team stylized city-silhouette WebP images from v0.9 (not photo-realistic stock photographs).
- Browser rotation per team remains 1–2–3–1 using localStorage.

## Quick install (recommended)

Replace only **`index.html`** in your NHL365 GitHub repository. This single-file update fixes the skyline loading problem even if `static/skylines/` was never uploaded.

If you prefer a complete application installation, the ZIP contains the Python server, logos, static skyline assets, tests and metadata as well. Do not delete current persistent storage or change Render start/build commands.

Render: `pip install -r requirements.txt` / `python NHL365_palvelin.py`.

Hard refresh your browser (`Ctrl+F5`) after the deployment.

## Validation
- 96 embedded WebP images, matching the local 96 assets.
- Browser validation with Chromium, calling set_content: Boston image loaded (`naturalWidth = 1200`) and the updated desktop/mobile header layout was measured. API calls are unavailable when rendering outside the running service.
- JavaScript syntax check using Node.js.
- Python compile check.
- All 14 Python regression tests passed.
- Actual public Render deployment remains to be tested by the repo owner.

# NHL365 v0.9 — Local Skyline Rotation

Built on **NHL365 v0.8** (which was built on NHL365 v0.7 / v0.6). No changes to the news, matches, team selection or English-language application data logic.

## What's new

- **96 local WebP skyline illustrations** (3 per NHL team), 1200 × 240 pixels each; total roughly 0.9 MB.
- The header skyline rotates **1 → 2 → 3 → 1** each time the app opens again in the same browser. Rotation counters are independent for each team.
- Changing teams also advances that team's own image selection.
- Removes live Wikimedia Commons API and external photo lookups entirely.
- Reduces the skyline height to **64px desktop / 50px tablet / 48px mobile**.
- `object-fit:contain` and the image composition avoid unwanted cropping; SVG fallback shows if an image cannot load.
- All UI labels remain in English; Team Colors styling and Change Team button are unchanged.

## Source files

- `index.html` — skyline selector, rotation, loading, CSS.
- `NHL365_palvelin.py` — serves `/static/skylines/<team>-<1..3>.webp` with validation, WebP content type and cache header.
- `static/skylines/` — 96 committed WebP files. **Commit the entire folder.**
- `data/skylines.json` — 32-team manifest and source metadata.
- `tools/generate_skylines.py` — reproducible image generator (requires Pillow only for offline development; *not* at Render runtime).
- `docs/SKYLINE_IMAGE_CREDITS.md` — description of image provenance.

## Install into NHL365 GitHub repository

Upload the **contents of the ZIP root** into the existing NHL365 repo. Replace `index.html` and `NHL365_palvelin.py` and add the entire `static/skylines/` directory. Keep the existing `logos` folder and other unchanged files.

Render settings stay the same:

    Build: pip install -r requirements.txt
    Start: python NHL365_palvelin.py

After deployment, test these URLs under your Render domain:

    /static/skylines/bos-1.webp
    /static/skylines/tor-2.webp
    /static/skylines/uta-3.webp

Use normal reload (F5) to see the skyline rotate. Browser `localStorage` must be enabled for continuity across visits. For a first-ever visit the first image is shown.

## Validation

- 96/96 image sizes and formats validated.
- 14 server regression tests pass.
- Rotation logic verified with Node.js.
- Python and JavaScript syntax verified.
- Image HTTP routes verified locally.

**Scope note:** Actual full browser-based Render visual testing remains to be completed after deployment. The images in this ZIP are stylized illustrations, not locally saved licensed city photographs; authentic photos would require separately obtaining suitable source images and maintaining attribution records.

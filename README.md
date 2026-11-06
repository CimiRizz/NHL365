# NHL365 v0.6 — Team Colors

Based on the working NHL365 v0.5 build. This is a **visual-only update**: news retrieval, NHL schedule, sources, team selection, local cache, article reader and English interface are preserved.

## What changed

- Consistent dark sport-themed page background, cards, selection dialog and article reader.
- One of 32 team-specific color palettes is applied immediately when selecting or changing teams.
- Team colors highlight header border, buttons, match cards, latest-news cards and active interactions.
- High-contrast light body copy on neutral dark panels, so white or yellow logos remain legible.
- Mobile responsiveness and reduced-motion preference preserved.
- Version footer now reads v0.6.

## Deploy

Only replace **index.html** in your NHL365 GitHub repository. Keep NHL365_palvelin.py, requirements.txt, logos and all other files as they are in v0.5. Render auto-deploys if enabled. Hard-refresh the browser afterward (Ctrl+F5).

## Validation

- Python tests from v0.5: 14/14 passed
- JavaScript parsed with node --check
- Team palette keys: 32/32
- No live-browser or deployed Render validation has been performed.

Team palette shades are practical UI accent choices, not exact official brand standards. All NHL and team logos remain owned by their respective rights holders.

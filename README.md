# NHL365 v0.4 – English interface and higher-contrast logos

Based on NHL365 v0.3. NHL365 remains a separate repository from Liiga365 and KalPa365.

## Updates
- Translated the entire visible web interface (team picker, next games, news, filters, reading dialog, errors and buttons) into English.
- Tampa Bay Lightning and Toronto Maple Leafs use NHL SVG `_light` variants on light cards (instead of white-on-white `_dark` artwork).
- Added a subtle pale-blue backing behind those two logos to maintain contrast.
- Dark header retains the `_dark` variant, which is suitable on black backgrounds.
- Same SVG -> bundled PNG -> abbreviation fallback as v0.3.
- No changes to news retrieval, schedule retrieval, team storage, or card layout.

## Install
Upload `index.html` to your NHL365 GitHub repository, replacing the previous file. Other files are included so this archive can also be used for a fresh deployment. Render start command: `python NHL365_palvelin.py`. Hard refresh with Ctrl+F5.

NHL brand assets belong to NHL and the teams. SVG reachability and exact styling should be confirmed in the deployed browser.

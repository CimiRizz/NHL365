# NHL365 v0.36 – All 32 City Panoramas

Ready-to-deploy application built on NHL365 v0.35 UI and v0.5 server.

- 32 team-specific local city panorama assets, 3 lighting variants each (96 images).
- Images are AI-generated stylized city concepts, NOT verified photographs.
- Some later batch collage sources include invented perspectives and were cropped to emphasize landmarks.
- The 3 variants for a team are different lighting grades of the same panorama, not 3 independent photographs.
- Loads images locally from `/static/cities/{team}-{variant}.webp`.
- If missing, original embedded skyline fallback is used.
- Preserves two-line team title, logos, Change Team puck, Refresh News, games and news features.

## GitHub / Render installation
Upload/rewrite the package's `index.html` and `NHL365_palvelin.py` and add the whole `static/cities/` directory. Keep your existing logos, requirements.txt, nhl_teams.json and other files.

Build Command: `pip install -r requirements.txt`
Start Command: `python NHL365_palvelin.py`

All 32 team codes and image variants are recorded in `static/cities/manifest.json`.

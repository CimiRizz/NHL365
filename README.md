# NHL365 v0.5 – 32 official NHL team news sources

This version is based on the working NHL365 v0.4. It preserves the English interface, team logos, latest-three localStorage cache, and schedule cards.

## News priority

1. Load the selected club’s official news page at `https://www.nhl.com/{club}/news/`.
2. Publish its article list immediately to `/api/news?team=...` with `phase=official_dates` while missing publication dates are checked in parallel.
3. Publish any newly recovered article dates and continue with the NHL.com and ESPN general RSS feeds. Their failure **never clears club news or saved articles**.
4. Each club gets its own server cache (five minutes). Only the currently selected club is fetched, avoiding 32 simultaneous source loads for normal users.

The old general RSS feeds remain secondary; official club stories do not require the club name in the headline. Article links are limited to the appropriate official NHL.com club news subtree. The existing distraction-free article reader works for these URLs.

## Club sources

All 32 are listed in `NHL365_palvelin.py` (`TEAM_SLUGS`). The names and logo identifiers remain in `nhl_teams.json`. Example: `uta` -> https://www.nhl.com/utah/news/.

## Deployment

Replace `NHL365_palvelin.py`, `index.html` and `requirements.txt` in the NHL365 repository. Build: `pip install -r requirements.txt`; start: `python NHL365_palvelin.py`. Keep the existing `logos/` directory.

## Check results

For a selected team, open `/api/news?team=tbl` and inspect `official_status`, `official_count`, `official_url` and `sources` after `refreshing` becomes false. `official_count` is the number of identified club articles on the page, not necessarily three articles with known publication dates. `official_status=error` means the site was unavailable; `no_articles` means the HTML response contained no qualifying article links.

**Live verification for all 32 teams:** run `python verify_render_sources.py https://YOUR-NHL365-SERVICE.onrender.com` on your Windows computer after deploying. This will check the real Render-facing scraper, NOT only the existence of each website. `python test_official_sources.py` probes the club sites directly from the machine running the script.

**Limit:** this authoring environment cannot connect directly to NHL servers to run the exact Python HTML scraper. All 32 NHL club news pages were researched on the web, but 32/32 **working scrapers** must be confirmed using the live verification tool. Do not claim unverified live success.

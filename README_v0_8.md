# NHL365 v0.8 — Team City Skyline Header

Based on the approved NHL365 v0.7 Team Colors application.

## Install

In your NHL365 GitHub repository, replace **only `index.html`** with the file in this ZIP. Leave `NHL365_palvelin.py`, `requirements.txt`, and the `logos` folder unchanged. Let Render deploy, then reload with Ctrl+F5.

## What's new

- A skyline panorama between the team name and Change Team button in the header.
- All 32 teams have individually mapped home-market skylines. NHL team names and city data remain in English.
- On team switch, the skyline, name, colors, and team logo update together.
- Fast, locally generated night-skyline SVG illustration is shown immediately. No service or extra file is required for the fallback.
- On supported browsers, the UI **tries** to find and show a freely licensed city skyline photograph from Wikimedia Commons. Images are selected by city, wide aspect ratio and license; the city photograph is not guaranteed for every team. A photo credit link is shown on the image if one loads.
- If image search/CORS fails, the illustration stays visible; no empty image or broken icon.
- Responsive desktop, tablet, and mobile arrangements.
- The existing v0.7 3D Change Team button and all v0.5 news/schedule functionality are preserved.

## Notes

- The illustrated skyline is a decorative rendering rather than a literal city photograph. Some landmarks are stylized for selected cities.
- Do not claim that photos for all 32 teams have been live-verified. The Wikimedia Commons API and image host are external services.
- A browser may decline external requests through a content blocker or network policy. The SVG fallback is self-contained and continues to work.
- City choices reflect home markets: for example Carolina -> Raleigh, Florida -> Fort Lauderdale, Minnesota -> Saint Paul, New Jersey -> Newark and Utah -> Salt Lake City.

## Verification

- All 32 team keys have skyline mappings.
- JavaScript syntax checked with Node.js.
- Existing server unit tests: 14/14 passing.
- Visual browser screenshots and live image retrieval were blocked by the environment; test in Render after deployment.

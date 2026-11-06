# NHL365 v0.1 (kehitysversio)

Oma GitHub-repositorio; lähtökohtana Liiga365 Baseline 1.0:n käyttöliittymä.

## Render

- Language: Python 3
- Build command: `pip install -r requirements.txt`
- Start command: `python NHL365_palvelin.py`
- Environment variable `PORT`: Render provides it automatically.

## Ominaisuudet

- Valinta kaikista 32 NHL-seurasta, tallennus selaimen localStorageen
- Viimeisten kolmen uutisen paikallinen välimuisti
- Vaiheittainen RSS-uutishaku (NHL.com ja ESPN NHL; saatavuus tarkistettava Renderissä)
- NHL:n julkisesta joukkuekohtaisesta kausirajapinnasta 3 seuraavaa ottelua
- Lukutila saatavissa oleville julkisille artikkeleille

## Rajapinnat

- `/api/teams`
- `/api/news?team=tor`
- `/api/matches?team=tor`
- `/api/article?url=https%3A...`

## Rajoitukset

V0.1 on tekninen pilottiversio, ei tuotantovalmis uutiskerääjä. Seurojen omia
verkkosivuja ei vielä haeta erikseen. NHL.com:n ja ESPN:n julkisten RSS-syötteiden
saatavuutta ei ole vahvistettu Renderissä. Joukkueuutisia voi jäädä löytämättä.
NHL:n logot eivät vielä sisälly pakettiin; käytössä on NHL365:n yleinen tunnus.

KalPa365:n ja Liiga365:n nykyisiä repoja, brancheja ja julkaisuja ei muuteta.

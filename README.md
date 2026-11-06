# NHL365 v0.3 – SVG-logot ja Utah Mammoth

Perustuu NHL365 v0.2:een. Tämä on NHL365:n **oma** projekti, ei muuta KalPa365:ttä tai Liiga365:tä.

## Päivitys v0.2 -> v0.3

- NHL:n joukkueiden SVG-logot ladataan suoraan NHL:n kuvapalvelimelta `https://assets.nhle.com/logos/nhl/svg/`.
- Utah Mammoth käyttää tunnusta `UTA`, eikä vanhaa Arizona Coyotes -logoa käytetä.
- Virallisia SVG-logoja käytetään joukkuevalinnassa, ottelukorteissa ja valitun joukkueen otsakelogossa; NHL-kilvelle on oma SVG-osoite.
- Jos SVG ei lataudu, sovellus kokeilee paikallista PNG:tä (Utahille ei ole PNG-varalogoja); jos sekään ei lataudu, näytetään joukkuekoodi.
- `logos/`-kansio on mukana vain varakuvia varten. Joukkueen teksti näkyy silloinkin, kun kuvat eivät lataudu.
- Ei muutoksia uutis- tai ottelurajapintaan.

## Asennus GitHub / Render

Lataa kaikki tämän ZIPin tiedostot **NHL365-repositorion juureen**. Korvaa `index.html`, pidä `NHL365_palvelin.py` ja `logos/` mukana. Renderin asetukset:

- Build: `pip install -r requirements.txt`
- Start: `python NHL365_palvelin.py`

Päivitä selaimessa Ctrl+F5. Testaa joukkuevalinnassa Utah Mammoth, Toronto ja Boston sekä seuraavien ottelujen logot.

## Kuvalähteet ja rajoitus

SVG:tä ei voitu ladata testikoneeseen verkkoyhteyden rajoituksen vuoksi. Koodi käyttää NHL:n julkisesti dokumentoitua SVG-osoitemallia, mutta kaikkien 32 tiedoston Render-/selaintoimivuutta ei ole vahvistettu. Fallback on tämän vuoksi mukana.

Tunnukset ja joukkueiden logot ovat NHL:n ja seurojen tavaramerkkejä; julkisen palvelun käyttöoikeudet on syytä selvittää.

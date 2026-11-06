"""NHL365 v0.1: independent, lightweight NHL news and schedule service.

NHL365 does not modify or connect to KalPa365 / Liiga365 deployments.
Uses the publicly documented NHL team schedule endpoint and public news RSS.
"""
from __future__ import annotations
import calendar
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock, Thread
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen
import concurrent.futures
import json
import os
import re
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
TEAMS = {item['id']: item for item in json.loads((ROOT/'nhl_teams.json').read_text())}
NEWS_RSS = {
    'ESPN NHL': 'https://www.espn.com/espn/rss/nhl/news',
    'NHL.com': 'https://www.nhl.com/rss/news',
}
# Team names and distinctive franchise names used for classification. A generic
# city alone is intentionally not enough to classify unrelated city news.
ALIASES = {
 'ana':['Ducks'], 'bos':['Bruins'], 'buf':['Sabres'], 'car':['Hurricanes'],
 'cbj':['Blue Jackets'], 'cgy':['Flames'], 'chi':['Blackhawks'],
 'col':['Avalanche'], 'dal':['Stars'], 'det':['Red Wings'],
 'edm':['Oilers'], 'fla':['Panthers'], 'lak':['Kings'], 'min':['Wild'],
 'mtl':['Canadiens', 'Habs'], 'njd':['Devils'], 'nsh':['Predators'],
 'nyi':['Islanders'], 'nyr':['Rangers'], 'ott':['Senators'],
 'phi':['Flyers'], 'pit':['Penguins'], 'sea':['Kraken'],
 'sjs':['Sharks'], 'stl':['Blues'], 'tbl':['Lightning'],
 'tor':['Maple Leafs'], 'uta':['Mammoth'], 'van':['Canucks'],
 'vgk':['Golden Knights'], 'wpg':['Jets'], 'wsh':['Capitals'],
}
NEWS_CACHE = {key: {'articles':[], 'refreshing':False, 'phase':'ready', 'updated':None, 'errors':[]} for key in TEAMS}
MATCH_CACHE = {}
NEWS_LOCK = Lock()


def fetch(url, limit=1_500_000, timeout=8):
    if not url.startswith('https://'):
        raise ValueError('Only HTTPS sources allowed')
    req = Request(url, headers={'User-Agent':'Mozilla/5.0 (compatible; NHL365/0.1; public news aggregator)', 'Accept':'application/json, application/rss+xml, text/html;q=0.8'})
    with urlopen(req, timeout=timeout) as res:
        return res.read(limit).decode('utf-8', errors='replace')


def team_match(team, title):
    text=title.casefold()
    full=TEAMS[team]['name'].casefold()
    if full in text: return True
    return any(re.search(r'(?<!\w)'+re.escape(alias.casefold())+r'(?!\w)', text) for alias in ALIASES[team])


def parse_feed(xml_text, source, team):
    root=ET.fromstring(xml_text)
    result=[]
    for item in root.findall('.//item'):
        title=' '.join((item.findtext('title') or '').split())
        if not title or not team_match(team,title):continue
        url=(item.findtext('link') or '').strip()
        if not url.startswith('https://'):continue
        date=item.findtext('pubDate')
        try: ts=int(parsedate_to_datetime(date).timestamp())
        except (TypeError,ValueError,OverflowError):ts=0
        desc=re.sub(r'<[^>]+>',' ',item.findtext('description') or '')
        desc=re.sub(r'\s+',' ',desc).strip()[:800]
        result.append({'title':title,'url':url,'source':source,'timestamp':ts,'summary':desc})
    return result


def distinct_sorted(entries):
    by_url={}
    for item in entries:
        if item.get('url') and item.get('title'):
            before=by_url.get(item['url'])
            if not before or item.get('timestamp',0)>=before.get('timestamp',0):by_url[item['url']]=item
    return sorted(by_url.values(),key=lambda x:x.get('timestamp',0),reverse=True)[:80]


def _refresh_news(team):
    errors=[]
    collected=[]
    # Stage 1: the league-owned RSS, if it is publicly available.
    try:
        collected+=parse_feed(fetch(NEWS_RSS['NHL.com']),'NHL.com',team)
    except Exception as e:
        errors.append('NHL.com: '+type(e).__name__)
    with NEWS_LOCK:
        s=NEWS_CACHE[team]
        s['articles']=distinct_sorted(s['articles']+collected)
        s['phase']='media'
    # Stage 2: publisher RSS feeds. Failures never overwrite cached items.
    try:
        collected+=parse_feed(fetch(NEWS_RSS['ESPN NHL']),'ESPN NHL',team)
    except Exception as e:
        errors.append('ESPN NHL: '+type(e).__name__)
    with NEWS_LOCK:
        s=NEWS_CACHE[team]
        s['articles']=distinct_sorted(s['articles']+collected)
        s['phase']='ready'
        s['refreshing']=False
        s['updated']=datetime.now(timezone.utc).isoformat()
        s['errors']=errors


def news_for(team):
    with NEWS_LOCK:
        s=NEWS_CACHE[team]
        expired = not s['updated'] or (time.time()-datetime.fromisoformat(s['updated']).timestamp()>300)
        if expired and not s['refreshing']:
            s['refreshing']=True
            s['phase']='official'
            Thread(target=_refresh_news,args=(team,),daemon=True).start()
        return {'status':'loading' if s['refreshing'] else 'ok', 'team':team, 'articles':list(s['articles']),
            'refreshing':s['refreshing'], 'phase':s['phase'], 'partial':s['refreshing'],
            'updated':s['updated'], 'errors':list(s['errors']),
            'sources':{key:{'status':'ok' if key not in ' '.join(s['errors']) else 'error'} for key in NEWS_RSS}}


def schedule_for(team):
    now=time.time()
    cached=MATCH_CACHE.get(team)
    if cached and now-cached[0]<900:return cached[1]
    code=TEAMS[team]['code']
    url=f'https://api-web.nhle.com/v1/club-schedule-season/{code}/now'
    try:
        raw=json.loads(fetch(url,limit=2_500_000,timeout=9))
        games=[]
        for g in raw.get('games',[]):
            if g.get('gameState') not in ('FUT','PRE','LIVE','CRIT'):continue
            iso=g.get('startTimeUTC')
            if not iso:continue
            try:dt=datetime.fromisoformat(iso.replace('Z','+00:00')).timestamp()
            except ValueError:continue
            if dt<now-10800:continue
            home=g.get('homeTeam',{}).get('abbrev','')
            away=g.get('awayTeam',{}).get('abbrev','')
            lookup={t['code']:t['name'] for t in TEAMS.values()}
            games.append({'date':iso,'home':lookup.get(home,home),'away':lookup.get(away,away),
              'venue':(g.get('venue') or {}).get('default','')})
        games.sort(key=lambda x:x['date'])
        result={'status':'ok','games':games[:3], 'source':'NHL API'}
        MATCH_CACHE[team]=(now,result)
        return result
    except Exception as e:
        if cached:return {**cached[1], 'error':type(e).__name__}
        return {'status':'error','games':[], 'error':type(e).__name__}

class ArticleText(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.text=[];self.capture=False
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','nav','footer','header'):self.depth+=1
        if tag=='p' and not self.depth:self.capture=True
    def handle_endtag(self,tag):
        if tag in ('script','style','nav','footer','header') and self.depth:self.depth-=1
        if tag=='p':self.capture=False;self.text.append('\n')
    def handle_data(self,data):
        if self.capture and not self.depth:self.text.append(data)

ALLOWED_ARTICLE_DOMAINS={'nhl.com','www.nhl.com','espn.com','www.espn.com'}
def article_for(url):
    parsed=urlparse(url)
    if parsed.scheme!='https' or parsed.hostname not in ALLOWED_ARTICLE_DOMAINS:
        return {'status':'summary','paragraphs':[], 'message':'Avaa artikkeli alkuperäiseltä sivulta.'}
    try:
        html=fetch(url,limit=1_200_000,timeout=8)
        parser=ArticleText();parser.feed(html)
        paragraphs=[re.sub(r'\s+',' ',s).strip() for s in ''.join(parser.text).split('\n')]
        paragraphs=[p for p in paragraphs if len(p)>45][:30]
        if paragraphs:return {'status':'full','paragraphs':paragraphs,'original_url':url}
    except Exception: pass
    return {'status':'summary','paragraphs':[], 'original_url':url,
            'message':'Tekstiä ei voitu hakea. Avaa artikkeli alkuperäiseltä sivulta.'}

class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200);self.end_headers()
    def do_GET(self):
        parsed=urlparse(self.path)
        path=parsed.path
        if path in ('/','/index.html'):
            body=(ROOT/'index.html').read_bytes();typ='text/html; charset=utf-8'
        elif path.startswith('/logos/'):
            # Serve only known local PNG assets. Path normalization prevents traversal.
            filename=path[len('/logos/'):]
            if not re.fullmatch(r'[A-Z0-9_]+\.png', filename):
                self.send_error(404);return
            asset=ROOT/'logos'/filename
            if not asset.is_file():
                self.send_error(404);return
            body=asset.read_bytes();typ='image/png'
        elif path=='/nhl365-logo.svg':
            body=(ROOT/'nhl365-logo.svg').read_bytes();typ='image/svg+xml'
        elif path=='/health':
            body=b'{"status":"ok"}';typ='application/json'
        elif path in ('/api/news','/api/matches','/api/teams','/api/article'):
            q=parse_qs(parsed.query)
            team=q.get('team',['tor'])[0].lower()
            if path=='/api/teams':data={'teams':list(TEAMS.values())}
            elif path=='/api/article':data=article_for(q.get('url',[''])[0])
            elif team not in TEAMS:
                self.send_error(400,'Unknown team');return
            elif path=='/api/news':data=news_for(team)
            else:data=schedule_for(team)
            body=json.dumps(data,ensure_ascii=False).encode('utf-8');typ='application/json'
        else:
            self.send_error(404);return
        self.send_response(200)
        self.send_header('Content-Type',typ)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store' if path.startswith('/api/') else 'public, max-age=60')
        self.end_headers()
        self.wfile.write(body)

if __name__=='__main__':
    port=int(os.environ.get('PORT','5000'))
    print(f'NHL365 http://localhost:{port}',flush=True)
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()

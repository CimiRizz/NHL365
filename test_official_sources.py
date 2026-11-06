"""Run locally or on Render (Shell) to check live official news coverage for all 32 clubs.

python test_official_sources.py
Exit code 1 if any club yields zero recognized official news items.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from NHL365_palvelin import TEAMS, official_news_url, parse_official_news, fetch


def check(team):
    url=official_news_url(team)
    try:
        stories=parse_official_news(fetch(url,limit=3_000_000,timeout=12),team)
        return team,len(stories),url,'' if stories else 'No article links found'
    except Exception as exc:
        return team,0,url,f'{type(exc).__name__}: {str(exc)[:90]}'


def main():
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(check,t) for t in TEAMS]
        results=sorted((f.result() for f in as_completed(futures)),key=lambda x:x[0])
    print('Team | Articles | Official news URL | Error')
    for team,n,url,error in results:
        print(f'{TEAMS[team]["code"]:<4} | {n:<8} | {url} | {error}')
    working=sum(n>0 for _,n,_,_ in results)
    print(f'RESULT: {working}/32 official club sources returned articles.')
    return 0 if working==32 else 1

if __name__=='__main__':
    raise SystemExit(main())

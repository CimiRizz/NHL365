"""Live audit: python verify_render_sources.py https://your-nhl365.onrender.com

Triggers and polls each club's official-news scan on your deployed Render instance.
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlencode
from urllib.request import urlopen
from NHL365_palvelin import TEAMS

BASE=(sys.argv[1] if len(sys.argv)>1 else '').rstrip('/')
if not BASE.startswith('https://'):
    raise SystemExit('Usage: python verify_render_sources.py https://your-service.onrender.com')


def audit(team):
    url=BASE+'/api/news?'+urlencode({'team':team})
    error=''
    for n in range(22):
        try:
            with urlopen(url,timeout=25) as r:
                data=json.loads(r.read())
            status=data.get('official_status','unknown')
            count=data.get('official_count',0)
            if status in ('ok','error','no_articles') and (not data.get('refreshing') or count>0):
                return team,status,count,data.get('official_url',''),'; '.join(data.get('errors',[]))
        except Exception as e:
            error=f'{type(e).__name__}: {e}'
        time.sleep(2.5)
    return team,'timeout',0,'',error or 'No completed response'


def main():
    print('Checking the deployed NHL365 official sources; please allow several minutes.',flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(audit,t):t for t in TEAMS}
        results=sorted((f.result() for f in as_completed(jobs)),key=lambda x:x[0])
    for team,status,count,url,err in results:
        print(f'{TEAMS[team]["code"]:<4} {status:<12} {count:>2} {url} {err}')
    good=sum(status=='ok' and count>0 for _,status,count,_,_ in results)
    print(f'OFFICIAL NEWS: {good}/{len(results)} teams returned at least one article')
    return 0 if good==len(results) else 1
if __name__=='__main__':raise SystemExit(main())

import unittest
from unittest.mock import patch
import NHL365_palvelin as nhl

SAMPLE='''<html><a href="/lightning/news/team-prepares-for-game"><span>Morning Skate: Today's lineup</span></a><time datetime="2026-11-06T09:00:00Z">Nov 06, 2026</time><a href="https://www.nhl.com/lightning/news/player-signs-contract">Player signs a new contract Nov 05, 2026</a><a href="/bruins/news/wrong-team">Unrelated team article</a><a href="/lightning/schedule">Not news</a></html>'''

class Tests(unittest.TestCase):
    def test_all_32_clubs_have_unique_verified_paths(self):
        self.assertEqual(len(nhl.TEAM_SLUGS),32)
        self.assertEqual(len(set(nhl.TEAM_SLUGS.values())),32)
        for team in nhl.TEAMS:
            self.assertTrue(nhl.official_news_url(team).startswith('https://www.nhl.com/'))
    def test_own_news_does_not_need_team_in_title(self):
        a=nhl.parse_official_news(SAMPLE,'tbl')
        self.assertEqual(len(a),2)
        self.assertTrue(a[0]['title'].startswith('Morning Skate'))
        self.assertEqual(a[0]['source'],'Tampa Bay Lightning (Official)')
        self.assertGreater(a[1]['timestamp'],0)
    def test_other_team_url_is_not_accepted(self):
        self.assertEqual(nhl.parse_official_news(SAMPLE,'bos'),[{'title':'Unrelated team article','url':'https://www.nhl.com/bruins/news/wrong-team','source':'Boston Bruins (Official)','timestamp':0,'summary':''}])
    def test_unrelated_or_unsafe_links_skipped(self):
        a=nhl.parse_official_news('<a href="https://evil.com/lightning/news/abc">bad</a><a href="javascript:alert(1)">bad</a><a href="/lightning/news/real-article">Great player signs deal</a>','tbl')
        self.assertEqual(len(a),1)
    def test_date_formats(self):
        self.assertEqual(nhl.date_timestamp('Nov 06, 2026'),nhl.date_timestamp('2026-11-06T00:00:00Z'))
        self.assertEqual(nhl.date_timestamp(''),0)
    def test_enrichment_date(self):
        self.assertGreater(nhl.article_meta_date('<meta property="article:published_time" content="2026-11-05T12:00:00Z">'),0)
    def test_official_first_even_when_media_unavailable(self):
        def fake_fetch(url,**kw):
            if url.endswith('/lightning/news/'):return SAMPLE
            if '/lightning/news/' in url:return '<meta property="article:published_time" content="2026-11-06T09:00:00Z">'
            raise OSError('offline')
        with patch.object(nhl,'fetch',side_effect=fake_fetch):
            nhl._refresh_news('tbl')
        items=nhl.NEWS_CACHE['tbl']['articles']
        self.assertEqual(len(items),2)
        self.assertEqual(nhl.NEWS_CACHE['tbl']['official_count'],2)
        self.assertEqual(nhl.NEWS_CACHE['tbl']['phase'],'ready')
        self.assertFalse(nhl.NEWS_CACHE['tbl']['refreshing'])
    def test_utah_current_slug(self):
        self.assertEqual(nhl.official_news_url('uta'),'https://www.nhl.com/utah/news/')

if __name__=='__main__':unittest.main()

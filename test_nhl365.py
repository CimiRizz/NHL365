import unittest
import NHL365_palvelin as app
class TestNHL365(unittest.TestCase):
    def test_team_count(self): self.assertEqual(len(app.TEAMS),32)
    def test_current_utah(self): self.assertEqual(app.TEAMS['uta']['name'],'Utah Mammoth')
    def test_team_match(self):
        self.assertTrue(app.team_match('tor','Toronto Maple Leafs beat the Bruins'))
        self.assertFalse(app.team_match('tor','Maple syrup season in Ontario'))
        self.assertTrue(app.team_match('uta','Utah Mammoth add forward'))
    def test_feed(self):
        feed='''<rss><channel><item><title>Toronto Maple Leafs beat Boston</title><link>https://www.nhl.com/news/a</link><pubDate>Thu, 05 Nov 2026 12:00:00 GMT</pubDate></item></channel></rss>'''
        got=app.parse_feed(feed,'NHL.com','tor')
        self.assertEqual(len(got),1);self.assertGreater(got[0]['timestamp'],0)
        self.assertEqual(app.parse_feed(feed,'NHL.com','ana'),[])
    def test_sort(self):
        news=[{'title':'a','url':'https://x/a','timestamp':1},{'title':'b','url':'https://x/b','timestamp':2}]
        self.assertEqual(app.distinct_sorted(news)[0]['title'],'b')
    def test_reject_article_hosts(self):
        self.assertEqual(app.article_for('http://127.0.0.1/private')['status'],'summary')
if __name__=='__main__':unittest.main()

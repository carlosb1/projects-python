import unittest
from unittest.mock import MagicMock
from app.github_service import GitHubStatsService
from domain import Bunch, URLEntry


class TestCrawlerManager(unittest.TestCase):
    def read_from_file(self, filename):
        with open(filename) as f:
            return f.read()
        return None

    def test_should_get_stats_when_web_is_loaded(self):
        mockedResponse = Bunch(status_code=200, text=self.read_from_file('./resources/stadistics.json'))
        service = GitHubStatsService()
        service.client.get = MagicMock(return_value=mockedResponse)
        values = service.crawl(['1.1.1.1'], [URLEntry('http://example')], ['http://api.example'])[0].languages
        self.assertEquals(2, len(values))
        self.assertAlmostEqual(13.34, values['C'], delta=0.01)
        self.assertAlmostEqual(86.65, values['Assembly'], delta=0.01)

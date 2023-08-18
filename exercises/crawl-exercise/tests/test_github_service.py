import unittest
from unittest.mock import MagicMock
import urllib
from app.github_service import GithubService, API_GITHUB_REPO, API_GITHUB_ISSUES
from domain import Bunch, Type, CrawlError, URLEntry


MOCK_STADISTICS = {'Assembly': 86.65767328322734, 'C': 13.342326716772659}
URL_TEST = [URLEntry('https://github.com/nodejs/help', 'nodejs', MOCK_STADISTICS).to_dict(), URLEntry('https://github.com/jupyter/help', 'jupyter', MOCK_STADISTICS).to_dict()]
URL_TEST_WIKIS = [URLEntry('https://github.com/nodejs/help/wiki').to_dict(), URLEntry('https://github.com/jupyter/help/wiki').to_dict()]
URL_TEST_ISSUES = [URLEntry('https://github.com/KleoPetroff/dev-log/issues/5').to_dict(), URLEntry('https://github.com/csawtelle/mlhq.io/issues/298').to_dict()]


class TestGithubService(unittest.TestCase):
    def read_from_file(self, filename):
        with open(filename) as f:
            return f.read()
        return None

    def setUp(self):
        self.github_service = GithubService()

    def test_should_return_repositories_when_it_finds(self):
        mockedResponse = Bunch(status_code=200, text=self.read_from_file('./resources/repositories_help_small.json'))
        mockedResponseStats = Bunch(status_code=200, text=self.read_from_file('./resources/stadistics.json'))
        self.github_service.client.get = MagicMock()
        self.github_service.client.get.side_effect = [mockedResponse, mockedResponseStats, mockedResponseStats]
        urls = self.github_service.crawl(['194.126.37.94:8080'], ['anyvalue'], Type.REPOSITORY.value)
        self.github_service.client.get.call_args(API_GITHUB_REPO, urllib.parse.quote_plus(' '.join('anyvalue')))
        self.assertEquals(URL_TEST, [url_entry.to_dict() for url_entry in urls])

    def test_should_return_error_when_it_receives_error(self):
        mockedResponse = Bunch(status_code=400, text='')
        self.github_service.client.get = MagicMock(return_value=mockedResponse)
        with self.assertRaises(CrawlError):
            self.github_service.crawl(['194.126.37.94:8080'], ['anyvalue'], Type.REPOSITORY.value)

    def test_should_return_issues_when_it_finds(self):
        mockedResponse = Bunch(status_code=200, text=self.read_from_file('./resources/issues_help_small.json'))
        self.github_service.client.get = MagicMock(return_value=mockedResponse)
        urls = self.github_service.crawl(['194.126.37.94:8080'], ['anyvalue'], Type.ISSUE.value)
        self.github_service.client.get.call_args(API_GITHUB_ISSUES, urllib.parse.quote_plus(' '.join('anyvalue')))
        self.assertEquals(URL_TEST_ISSUES, [url_entry.to_dict() for url_entry in urls])

    def test_should_return_wikis_when_it_finds(self):
        mockedResponse = Bunch(status_code=200, text=self.read_from_file('./resources/repositories_help_small.json'))
        self.github_service.client.get = MagicMock(return_value=mockedResponse)
        urls = self.github_service.crawl(['194.126.37.94:8080'], ['anyvalue'], Type.WIKI.value)
        self.assertEquals(URL_TEST_WIKIS, [url_entry.to_dict() for url_entry in urls])

    def test_should_return_wikis_not_proxies_available(self):
        mockedResponse = Bunch(status_code=200, text=self.read_from_file('./resources/repositories_help_small.json'))
        self.github_service.client.get = MagicMock(return_value=mockedResponse)
        with self.assertRaises(CrawlError):
            self.github_service.crawl([], ['anyvalue'], Type.WIKI)

    def test_should_return_error_when_it_receives_error_rate_limit(self):
        headers = {}
        headers['X-RateLimit-Remaining'] = 0
        mockedResponse = Bunch(status_code=403, text='', headers=headers)
        self.github_service.client.get = MagicMock(return_value=mockedResponse)
        with self.assertRaises(CrawlError):
            self.github_service.crawl(['194.126.37.94:8080'], ['anyvalue'], Type.REPOSITORY.value)

    def test_should_return_error_when_it_receives_error_abuse_rate_limit(self):
        headers = {}
        headers['X-RateLimit-Remaining'] = 10
        mockedResponse = Bunch(status_code=403, text=self.read_from_file('./resources/error_abuse.json'), headers=headers)
        self.github_service.client.get = MagicMock(return_value=mockedResponse)
        with self.assertRaises(CrawlError):
            self.github_service.crawl(['194.126.37.94:8080'], ['anyvalue'], Type.REPOSITORY)

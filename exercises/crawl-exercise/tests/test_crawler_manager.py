import unittest
from unittest.mock import MagicMock
from collections import namedtuple
import json
from app.crawler_manager import CrawlerManager
from app.github_service import GithubService
from domain import Bunch


class TestCrawlerManager(unittest.TestCase):
    def read_from_file(self, filepath):
        fil = open(filepath)
        info = fil.read()
        fil.close()
        return info

    def json_to_object(self, inpt):
        return json.loads(inpt, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def test_should_run_crawl_when_it_receives_params(self):
        github_service = GithubService()
        entry_result = {}
        entry_result['url'] = 'http://example.com'
        github_service.crawl = MagicMock(return_value=[entry_result])
        crawlerManager = CrawlerManager(github_service)

        query = Bunch(proxies=['1.1.1.1'], type='Any', keywords=['test1'])
        result = crawlerManager.run(query)
        self.assertIsNotNone(result)
        self.assertEquals(result, [entry_result])

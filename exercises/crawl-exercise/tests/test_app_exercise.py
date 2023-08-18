import unittest
import io
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import MagicMock
from app.app import App
from app.crawler_manager import CrawlerManager
from app.domain import URLEntry, CrawlError

OUTPUT1 = '[{"url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage"}]'
OUTPUT_NOT_KEYWORDS = 'It is necessary include keywords in the query\n'
OUTPUT_NOT_PROXIES = 'It is necessary include proxies in the query\n'
OUTPUT_NOT_TYPES = 'It is necessary include types in the query\n'
OUTPUT_ERROR = "It ocurred an error in the crawl process"


class TestApp(unittest.TestCase):
    def test_should_not_execute_crawl_when_it_does_not_have_params(self):
        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            my_args = []
            mocked_crawler_manager = MagicMock()
            app = App(mocked_crawler_manager)
            with self.assertRaises(SystemExit):
                app.run(my_args)
            self.assertEquals("usage: nosetests [-h] file\nnosetests: error: the following arguments are required: file\n", buf.getvalue())

    def test_should_execute_crawl_when_it_has_params(self):
        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            my_args = ['./resources/input1.json']
            mocked_crawler_manager = CrawlerManager(None, None)
            mocked_crawler_manager.run = MagicMock(return_value=[URLEntry("https://github.com/atuldjadhav/DropBox-Cloud-Storage")])
            app = App(mocked_crawler_manager)
            app.run(my_args)
            self.assertEquals(OUTPUT1 + '\n', buf.getvalue())

    def test_should_execute_not_crawl_when_it_does_not_have_keywords(self):
        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            my_args = ['./resources/not_params.json']
            mocked_crawler_manager = MagicMock()
            app = App(mocked_crawler_manager)
            app.run(my_args)
            self.assertEquals(OUTPUT_NOT_KEYWORDS, buf.getvalue())

    def test_should_execute_not_crawl_when_it_does_not_have_proxies(self):
        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            my_args = ['./resources/not_proxies.json']
            mocked_crawler_manager = MagicMock()
            app = App(mocked_crawler_manager)
            app.run(my_args)
            self.assertEquals(OUTPUT_NOT_PROXIES, buf.getvalue())

    def test_should_execute_not_crawl_when_it_does_not_have_types(self):
        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            my_args = ['./resources/not_types.json']
            mocked_crawler_manager = MagicMock()
            app = App(mocked_crawler_manager)
            app.run(my_args)
            self.assertEquals(OUTPUT_NOT_TYPES, buf.getvalue())
          
    def test_should_return_manage_error_when_it_can_not_connect(self):
        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            my_args = ['./resources/input1.json']
            mocked_crawler_manager = CrawlerManager(None, None)
            mocked_crawler_manager.run = MagicMock(side_effect=CrawlError('Example'))
            app = App(mocked_crawler_manager)
            app.run(my_args)
            self.assertTrue(buf.getvalue().startswith(OUTPUT_ERROR))

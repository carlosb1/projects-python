import sys
import argparse
import json
import os
from collections import namedtuple
sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from crawler_manager import CrawlerManager
from github_service import GithubService


class App():
    def __init__(self, crawler_manager):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('file', help='read from file json input information', type=argparse.FileType('r'))
        self.crawler_manager = crawler_manager

    def json_to_object(self, inpt):
        return json.loads(inpt, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def parse_from_file(self, fil):
        read_data = fil.read()
        fil.close()
        return read_data

    def run(self, args):
        self.parsed_args = vars(self.parser.parse_args(args))
        inpt = self.parse_from_file(self.parsed_args['file'])
        query = self.json_to_object(inpt)
        if "keywords" not in dir(query):
            print("It is necessary include keywords in the query")
            return
        if "proxies" not in dir(query):
            print("It is necessary include proxies in the query")
            return

        if "type" not in dir(query):
            print("It is necessary include types in the query")
            return
        try:
            results = self.crawler_manager.run(query)
        except Exception:
            print("It ocurred an error in the crawl process")
        else:
            print(json.dumps([result.to_dict() for result in results]))


if __name__ == '__main__':
    github_service = GithubService()
    crawler_manager = CrawlerManager(github_service)
    App(crawler_manager).run(sys.argv[1:])

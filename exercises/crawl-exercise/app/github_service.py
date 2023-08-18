import requests
import json
import urllib
from domain import CrawlError, Type, URLEntry
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from proxy_service import ProxyService

API_GITHUB_REPO = 'https://api.github.com/search/repositories'
API_GITHUB_ISSUES = 'https://api.github.com/search/issues'
STATUS_GET_OK = 200
STATUS_GET_ERROR_RATE_LIMIT = 403
MSG_ERROR_ABUSE = 'You have triggered an abuse detection mechanism and have been temporarily blocked from content creation. Please retry your request again later.'


class APIService:
    def __init__(self):
        self.proxy_service = ProxyService()

    def check_error(self, response):
        return response.status_code != STATUS_GET_OK and response.status_code != STATUS_GET_ERROR_RATE_LIMIT

    def check_quote_rate_limit(self, response):
        return response.status_code == STATUS_GET_ERROR_RATE_LIMIT and response.headers['X-RateLimit-Remaining'] == 0

    def check_abuse_rate_limit(self, response):
        return MSG_ERROR_ABUSE in response.text


class GitHubStatsService(APIService):
    def __init__(self):
        super().__init__()
        self.client = requests

    def crawl(self, proxies, entries, api_urls):
        best_proxies = self.proxy_service.get_available_proxies(proxies)
        url_result = []
        for proxy in best_proxies:
            index = 0
            for entry in entries:
                url = api_urls[index] + '/languages'
                try:
                    response = self.client.get(url)
                except Exception:
                    continue
                if self.check_error(response):
                    raise CrawlError('Incorrect status code: status code=' + str(response.status_code) + ' text=' + str(response.text))
                if self.check_quote_rate_limit(response):
                    continue
                if self.check_abuse_rate_limit(response):
                    continue

                percentage = json.loads(response.text)

                saved_percentages = {}
                total = sum(percentage.values())
                for key in percentage.keys():
                    val = percentage[key]
                    saved_percentages[key] = (float(val) / float(total)) * 100.
                entry.languages = saved_percentages
                url_result.append(entry)
        return url_result


class GithubService(APIService):
    def __init__(self):
        super().__init__()
        self.client = requests
        self.stats_service = GitHubStatsService()

    def crawl(self, proxies, keywords, typ, number_page=1):
        terms = urllib.parse.quote_plus(' '.join(keywords))
        params = {'q': terms, 'page': number_page}
        url = API_GITHUB_REPO
        if Type.ISSUE == typ:
            url = API_GITHUB_ISSUES
        best_proxies = self.proxy_service.get_available_proxies(proxies)
        for proxy in best_proxies:
            proxyDict = {"https": proxy}
            response = self.client.get(url, params=params, proxys=proxyDict)
            if self.check_error(response):
                raise CrawlError('Incorrect status code: status code=' + str(response.status_code) + ' text=' + str(response.text))
            if self.check_quote_rate_limit(response):
                continue
            if self.check_abuse_rate_limit(response):
                continue
            json_text = json.loads(response.text)
            if Type.ISSUE.value == typ:
                urls = self.extract_urls_issue(json_text)
                return urls
            if Type.WIKI.value == typ:
                urls = self.extract_urls_wiki(json_text)
                return urls
            if Type.REPOSITORY.value == typ:
                urls = self.extract_urls_repository(json_text, proxies)
                return urls

        raise CrawlError('Any available proxy')

    def extract_urls_issue(self, json_text):
        return [URLEntry(item['html_url']) for item in json_text['items']]

    def extract_urls_wiki(self, json_text):
        urls = [item['html_url'] for item in json_text['items']]
        return [URLEntry(url_repo + '/wiki') for url_repo in urls]

    def extract_urls_repository(self, json_text, proxies):
        urls = [URLEntry(item['html_url'], item['owner']['login']) for item in json_text['items']]
        api_urls = [item['url'] for item in json_text['items']]
        return self.stats_service.crawl(proxies, urls, api_urls)

import concurrent.futures

WORKERS = 5


class CrawlerManager():
    def __init__(self, github_service, max_pages=1):
        self.github_service = github_service
        self.max_pages = max_pages

    def run(self, query):
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
            future_results = {executor.submit(self.github_service.crawl, query.proxies, query.keywords, query.type, number_page): number_page for number_page in range(1, self.max_pages + 1)}
            for future in concurrent.futures.as_completed(future_results):
                data = future.result()
                results.extend(data)
            return results

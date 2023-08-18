from random import shuffle


class ProxyService:
    def get_available_proxies(self, proxies):
        shuffle(proxies)
        return proxies

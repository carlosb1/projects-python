from enum import Enum


class Type(Enum):
    REPOSITORY = 'Repositories'
    ISSUE = 'Issues'
    WIKI = 'Wikis'


class URLEntry:
    def __init__(self, url, owner=None, languages=None):
        self.url = url
        self.owner = owner
        self.languages = languages

    def to_dict(self):
        result = {}
        result['url'] = self.url
        if not self.owner or not self.languages:
            return result

        extra = {}
        extra['owner'] = self.owner
        extra['language_stats'] = self.languages
        if len(extra) > 0:
            result['extra'] = extra
        return result


class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class CrawlError(Exception):
    def __init__(self, message=''):
        super().__init__()
        self.message = message

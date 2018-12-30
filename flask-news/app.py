from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_cors import cross_origin, CORS
import requests
from flask import request
from factory_responses import FactoryResponse
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from newspaper import Article
import newspaper
from celery import Celery


class ElasticSearchIndexer:
    def __init__(self, index_name):
        self.es = Elasticsearch()
        self.id = 1
        self.index_name = index_name

    def index(self, doc_type, doc):
        self.es.index(index=self.index_name, doc_type=doc_type, id=self.id, body=doc)
        self.id += 1

    def get(self, doc_type, _id):
        return self.es.get(index=self.index_name, doc_type=doc_type, id=_id)

    def search(self, doc_type, body):
        return self.es.search(index=self.index_name, doc_type=doc_type, body=body)


EXCLUDED_KEYS = ['config', 'extractor', 'html', 'article_html', 'meta_favicon', 'meta_data', 'top_node', 'clean_top_node', 'doc', 'clean_doc']
ELASTIC_KEYS = ['url', 'title', 'keywords', 'meta_keywords', 'tags', 'summary', 'link_hash']


def dict_from_class(cls, keys_to_analyse=[], included=False):
    return dict((key, value) for (key, value) in cls.__dict__.items() if ((key in keys_to_analyse) == included))


def extract_news_from_web(url_root, language):
    extracted_news = newspaper.build(url_root, language=language)
    return list(extracted_news.articles)


def get_collection(host, port):
    connection = MongoClient(host, port)
    db = connection['db_news']
    news = db['news']
    return news

USED_LANGUAGE = 'es'
CELERY_BROKER_ADDRESS = 'redis://localhost'

news = get_collection('localhost', 27017)
elastic_searcher = ElasticSearchIndexer('news')
app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")
celery = Celery('tasks', broker=CELERY_BROKER_ADDRESS)

# Configure CORS feature
cors = CORS(app, resources={r"/api/*": {"origins": '*'}})
app.config['CORS_HEADER'] = 'Content-Type'


@app.route('/api/news', methods=['GET'])
@cross_origin(origin='*')
def get_news():
    content = request.json
    tags = content['tags']
    query = {'query': {'match': tags}}
    # response = {'text_response': 'hello world'}
    results = elastic_searcher.search('new', query)
    return jsonify(results)


@app.route('/api/news', methods=['POST'])
@cross_origin(origin='*')
def post_news():
    content = request.json
    if 'urls' not in content or len(content['urls']) == 0:
        return FactoryResponse.new400()
    try:
        analyse_urls(content['urls'])
    except:
        return FactoryResponse.new500()

    return FactoryResponse.new201()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")


@celery.task
def run_batch(elastic_searcher, news, database_id, url):
        print("Executing analysed batch task")
        article = Article(url, language=USED_LANGUAGE)
        article.download()
        article.parse()
        article.nlp()

        # parse correctly db
        db_news = dict_from_class(article, EXCLUDED_KEYS)
        db_news['images'] = list(db_news['images'])
        db_news['imgs'] = list(db_news['imgs'])
        db_news['tags'] = list(db_news['tags'])
        db_news['timestamp'] = datetime.now()

        # parse correctly doc tags
        doc = dict_from_class(article, ELASTIC_KEYS, included=True)
        doc['tags'] = list(doc['tags'])
        print("Inserting url: " + doc['url'])
        doc['db_id'] = database_id
        doc['timestamp'] = datetime.now()
        news.update(db_news, upsert=True)
        elastic_searcher.index('new', doc)


def analyse_urls(urls):
    # we add to database
    for url in urls:
        if not news.find_one({'url': url}):
            database_id = str(news.insert_one({'url': url}).inserted_id)
            # run_batch(elastic_searcher, news, database_id, url)
            run_batch.apply_async((elastic_searcher, news, database_id, url))


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5001
    debug = False
    celery_argvs = ['worker', '--loglevel=DEBUG']
    # urls = []
    # url = 'https://www.lavanguardia.com/politica/20181217/453605810080/datos-marcaron-politica-2018.html'
    # urls.append(url)
    # analyse_urls(urls)

    import threading
    celery_thread = threading.Thread(target=celery.worker_main, args=[celery_argvs])
    celery_thread.start()
    app.run(host=host, port=port, debug=debug)

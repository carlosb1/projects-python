import filters
import utils
from celery import Celery
import os

path_config = os.getenv('DEMO_SILENT_CFG', default='ini.cfg')
var_configs = utils.load_config(path_config)
queue = Celery('tasks', broker=var_configs['CELERY_BROKER_ADDRESS'], include=['app'])
queue.start(argv=['celery', 'worker', '-l', 'debug'])

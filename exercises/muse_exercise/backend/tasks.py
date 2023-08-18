import os
from celery import Celery
import logging 
import filters
from utils import get_collection, generate_output_file, load_config
from bson.objectid import ObjectId
import traceback

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file = logging.FileHandler('celery.log')
log_file.setLevel(logging.DEBUG)
logger.addHandler(log_file)

# Variable configuration
path_config = os.getenv('DEMO_SILENT_CFG', default='ini.cfg')
var_configs = load_config(path_config)

# Set up batch worker
celery = Celery('tasks', broker=var_configs['CELERY_BROKER_ADDRESS'])

@celery.task
def run_batch(id_):
        logger.info("Executing analysed batch task")
        videos_db = get_collection(var_configs['MONGODB_HOST'], var_configs['MONGODB_PORT'])
        found_video = videos_db.find_one({'_id': ObjectId(id_)})
        if found_video:
            filepath = found_video['video_path']
            output_filepath = generate_output_file(filepath)
            logger.info("Analysing: "+ filepath + "creating: "+output_filepath)
            try:
                filters.delete_silent_file(filepath, output_filepath)
                videos_db.update_one({'_id': ObjectId(id_)}, {'$set': {'status':'SUCCESS'}}, upsert=False)
            except Exception as e:
                logger.error(traceback.format_exception(*sys.exc_info()))
                videos_db.update_one({'_id': ObjectId(id_)}, {'$set': {'status':'ERROR'}}, upsert=False)

        else:
            logger.warn("not found video with id: "+ str(id_))

from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_cors import cross_origin, CORS
import requests
from flask import request, send_from_directory
from factory_responses import FactoryResponse
import pymongo
from bson.objectid import ObjectId
import logging
import os
import uuid
import traceback
import sys
from utils import allowed_extension, create_new_directory, timestamp, generate_output_file, get_collection, load_config
from tasks import run_batch

# Variable configuration
path_config = os.getenv('DEMO_SILENT_CFG', default='ini.cfg')
var_configs = load_config(path_config)

# set up directory
create_new_directory(var_configs['DIRECTORY_VIDEO'])

# Set up web service
app = Flask(__name__)

# Set up factory for responses
factory_responses = FactoryResponse()

ROOT_API = var_configs['ROOT_API']
HOST = var_configs['HOST']
PORT = var_configs['PORT']

# Configure CORS feature
cors = CORS(app, resources={r'/v1/api/*': {"origins": '*'}})
app.config['CORS_HEADER'] = 'Content-Type'

# Logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file = logging.FileHandler('backend.log')
log_file.setLevel(logging.DEBUG)
logger.addHandler(log_file)
logger.info("Setting up API: "+ROOT_API + " host: "+HOST+ " port: "+str(PORT))


# POST function to upload a new video to analyse
@app.route(ROOT_API+'/videos', methods=['POST'])
@cross_origin(origin='*')
def post_videos():
    logger.info("Post a new video...")
    videos_db = get_collection(var_configs['MONGODB_HOST'], var_configs['MONGODB_PORT'])
    
    list_ids = []
    for key in request.files:
        fil = request.files[key]
        extension = fil.filename.rsplit('.',1)[1].lower()
        if not allowed_extension(extension):
            return factory_responses.new200();
        fil_identifier = timestamp() +"_"+ str(uuid.uuid4()) + "." + extension
        filepath = os.path.join(var_configs['DIRECTORY_VIDEO'], fil_identifier)
        fil.save(filepath) 
        insert_query = {'video_path': filepath, 'namefile': fil.filename, 'status': 'PENDING', 'result_video_path': filepath, 'last_modified': datetime.utcnow()}
        new_id = str(videos_db.insert_one(insert_query).inserted_id)
        list_ids.append(new_id)
        run_batch.apply_async([new_id])
    return factory_responses.new201({'ids': list_ids})

# GET function to list status of analysed videos
@app.route(ROOT_API+'/videos', methods=['GET'])
@cross_origin(origin='*')
def get_videos():
    logger.info("Getting list of videos...")
    # Getting args to change number of videos to response
    number_values = request.args.get('per_page', default=20, type=int)

    videos_db = get_collection(var_configs['MONGODB_HOST'], var_configs['MONGODB_PORT'])
    results = list(map(lambda x: {'id': str(x['_id']), 'namefile': x['namefile'], 'status': x['status'], 'last_modified': x['last_modified'], 'download_link': "http://"+HOST+":"+str(PORT) + ROOT_API+"/videos/"+str(x["_id"])+"/result"}, videos_db.find().sort('last_modified', pymongo.DESCENDING).limit(number_values)))
    return jsonify({'data': results, 'per_page': number_values})

# GET function to receive resulf from one video
@app.route(ROOT_API+'/videos/<new_id>/result', methods=['GET'])
@cross_origin(origin='*')
def download_result_videos(new_id):
    logger.info("Getting result video for id: "+str(new_id))
    videos_db = get_collection(var_configs['MONGODB_HOST'], var_configs['MONGODB_PORT'])
    found_video = videos_db.find_one({'_id': ObjectId(new_id)})

    if not found_video or found_video['status'] !='SUCCESS':
        return factory_responses.new200()
    filepath = found_video['video_path']
    filepath_output = generate_output_file(filepath)
    name_file = os.path.basename(filepath_output)
    directory = os.path.dirname(filepath_output)
    return send_from_directory(directory, name_file, as_attachment=True)

# Result for other requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return factory_responses.new200()


if __name__ == '__main__':
    logger.info("Running API REST")
    app.run(host=HOST, port=PORT, debug=var_configs['DEBUG'])

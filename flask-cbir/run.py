from flask import Flask, render_template, jsonify
from flask_cors import cross_origin, CORS
import requests
import os
import uuid
from flask import request
from factory_responses import FactoryResponse
from vgg16_img_search_engine import VGG16ImageSearchEngine
from random import randint
# PENDING TASKS
# [ ] -> Add pagination
# [ ] -> model correctly REST API

UPLOAD_DIRECTORY = 'uploads'
DIRECTORY_IMAGES = './frontend/static'
TOP_K = 20

# initialise database
engine = VGG16ImageSearchEngine()
app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")

# Configure CORS feature
cors = CORS(app, resources={r"/api/*": {"origins": '*'}})
app.config['CORS_HEADER'] = 'Content-Type'

import glob
for img_path in glob.iglob(DIRECTORY_IMAGES+os.sep+"*.jpg"):
    engine.index_image(img_path)

def timestamp():
    import time
    return str(time.time()).split(".")[0]

@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/api/images', methods=['POST'])
@cross_origin(origin='*')
def post_image():
    for key in request.files:
        fil = request.files[key]
        f_name = fil.filename
        filepath = os.path.join(DIRECTORY_IMAGES, f_name)
        fil.save(filepath)
        engine.index_image(filepath)
    # RUN BACKGROUND TASK TO RECEIVE result
    factory_response = FactoryResponse()
    return factory_response.new200()


# TODO Add search param
@app.route('/api/analysis', methods=['POST'])
@cross_origin(origin='*')
def post_new_analysis():
    fil = request.files['file']
    identifier = timestamp() + str(uuid.uuid4())
    extension = os.path.splitext(fil.filename)[1]
    f_name = identifier + extension
    filepath = UPLOAD_DIRECTORY + os.sep + f_name
    fil.save(filepath)
    result_top_values = engine.query_top_k(filepath, TOP_K)
    parsed_top_values = []

    #TODO do this in a clean way.
    for elem in result_top_values:
        complete_path = elem['path']
        relative_path = '/'.join(complete_path.split("/")[2:])
        elem['path'] = relative_path
        parsed_top_values.append(elem)
    # RUN BACKGROUND TASK TO RECEIVE result
    factory_response = FactoryResponse()
    res = factory_response.new201(parsed_top_values)
    return res


@app.route('/api/images', methods=['GET'])
def get_images():
    response = {'text_response': 'hello world'}
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

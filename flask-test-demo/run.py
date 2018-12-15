from flask import Flask, render_template, jsonify
import requests
import os
import uuid
from flask import request
from factory_responses import FactoryResponse
from vgg16_img_search_engine import VGG16ImageSearchEngine


UPLOAD_DIRECTORY = 'uploads'
TOP_K = 20

# initialise databae
engine = VGG16ImageSearchEngine()
app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")

import glob
for img_path in glob.iglob("./images/*.jpg"):
    engine.index_image(img_path)


def timestamp():
    import time
    return str(time.time()).split(".")[0]


@app.route('/api/images', methods=['POST'])
def post_image():
    fil = request.files['file']
    identifier = timestamp() + str(uuid.uuid4())
    extension = os.path.splitext(fil.filename)[1]
    f_name = identifier + extension
    filepath = os.path.join(UPLOAD_DIRECTORY, f_name)
    fil.save(filepath)
    engine.index_image(filepath)
    # RUN BACKGROUND TASK TO RECEIVE result
    factory_response = FactoryResponse()
    return factory_response.new201({'id': str(identifier)})


@app.route('/api/images/analysis', methods=['POST'])
def post_new_analysis():
    fil = request.files['file']
    identifier = timestamp() + str(uuid.uuid4())
    extension = os.path.splitext(fil.filename)[1]
    f_name = identifier + extension
    filepath = os.path.join(UPLOAD_DIRECTORY, f_name)
    fil.save(filepath)
    result_top_values = engine.query_top_k(filepath, TOP_K)
    # RUN BACKGROUND TASK TO RECEIVE result
    factory_response = FactoryResponse()
    return factory_response.new201({'id': str(result_top_values)})


@app.route('/api/images', methods=['GET'])
def random_number():
    response = {'text_response': 'hello world'}
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

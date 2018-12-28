from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import requests
from chatbot import WrapperChatbot
import eventlet
eventlet.monkey_patch()
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode="eventlet")

chatbot = WrapperChatbot()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080{}'.format(path)).text
    return render_template("index.html")

@socketio.on('connect')
def socketio_connect():
    print('Client has connected to the backend')
    emit('event', {'message': 'ACK'})


@socketio.on('event')
def socketio_message_event(message):
    print('Received event: ' + str(message.encode('utf-8')))
    response_message = chatbot.run(message)
    print(str(response_message))
    emit('response', {'message': response_message})

@socketio.on('response')
def socketio_message_response(message):
    print('Received response: ' + str(message.encode('utf-8')))


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5004
    debug = True
    socketio.run(app, host=host, port=port, debug=debug)

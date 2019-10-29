import threading

from flask import Flask, render_template, Response, session
import cv2 as cv

class Camera(object):
    def __init__(self, rtsp: str):
        self._rtsp = rtsp
        self._vcap = cv.VideoCapture(self._rtsp)

    def get_frame(self):
        ret, frame = self._vcap.read()
        return ret, frame


outputFrame = None
lock = threading.Lock()
camera = Camera('rtsp://admin:admin1234@10.0.70.2/cam/realmonitor?channel=1&subtype=2')

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


@app.route("/video_feed")
def video_feed():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        with lock:
            ret, frame = camera.get_frame()
            if not ret:
                continue
            frame = cv.resize(frame, (640, 380))
            (flag, frame) = cv.imencode(".jpg", frame)
            if not flag:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')


#def run_process(number):


if __name__ == '__main__':
    app.run(debug=True)

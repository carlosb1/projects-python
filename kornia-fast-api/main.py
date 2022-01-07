from fastapi import WebSocket
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from abc import ABC
#import numpy as np
#import cv2
import kornia
import base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# def image_to_base64(img: np.ndarray) -> bytes:
#     """ Given a numpy 2D array, returns a JPEG image in base64 format """
#
#     # using opencv 2, there are others ways
#     img_buffer = cv2.imencode('.jpg', img)[1]
#     return base64.b64encode(img_buffer).decode('utf-8')
#
#
# def get_image(volume, index: int):
#     image = volume[:, :, index]
#     return image_to_base64(image)
#

# @app.websocket("/ws"
# async def websocket_endpoint(websocket: WebSocket):
#    print("started")
#    await websocket.accept()
#    try:
#        while True:
#            data = await websocket.receive_text()
#            print(f"received: {int(data)}")
#            index = int(data)
#            image = get_image(volume, index)
#            await websocket.send_bytes(image)
#    except Exception as e:
#        print(e)
#    finally:
#        websocket.close()
#


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

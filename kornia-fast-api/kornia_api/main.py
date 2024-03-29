"""Main entrypoint function."""
from typing import List
from pathlib import Path

from fastapi import WebSocket
from fastapi import FastAPI, File
from fastapi.staticfiles import StaticFiles

import torch
import cv2
import base64
import uvicorn
import numpy as np
import kornia as K


# TODO add loggers


FILE_PATH = Path('image.jpg')


def image_to_base64(img: np.ndarray) -> bytes:
    """ Given a numpy 2D array, returns a JPEG image in base64 format """
    # using opencv 2, there are others ways
    _, img_buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(img_buffer).decode('utf-8')


def create_target_file_path(file_path: Path, count: int):
    target_file_path = Path(file_path.parent, file_path.stem +
                            str(count) + file_path.suffix)
    return target_file_path


class Controller:
    def save_files(self, byt_files: List[bytes], file_path: Path):
        for count, byt_fil in enumerate(byt_files):
            target_file_path = create_target_file_path(file_path, count)
            target_file_path.mkdir(parents=True, exist_ok=True)
            f = open(target_file_path, "wb")
            f.write(byt_fil)
            f.close()


controller = Controller()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@ app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    controller.save_files(files, FILE_PATH)
    return {"file_sizes": [len(file) for file in files]}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("started")
    await websocket.accept()
    try:
        while True:
            target_file_path = create_target_file_path(FILE_PATH, 0)
            if not target_file_path.is_file():
                print("Discard, it doesn t exist image")
            data = cv2.imread(str(target_file_path))
            x_bgr: torch.tensor = K.image_to_tensor(data)
            x_rgb: torch.tensor = K.color.bgr_to_rgb(x_bgr)
            img_rgb: np.array = K.tensor_to_image(x_rgb)
            image = image_to_base64(img_rgb)
            await websocket.send_bytes(image)
    except Exception as e:
        print(e)
    finally:
        websocket.close()


def run():
    uvicorn.run(app="kornia_api.main:app")


if __name__ == '__main__':
    run()

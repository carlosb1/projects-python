from typing import Optional
from fastapi import FastAPI, File, UploadFile

import torch
import kornia

app = FastAPI()


class KorniaController:
    def run(self):
        pass


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

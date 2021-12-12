from typing import Optional
from fastapi import FastAPI

import torch
import kornia

app = FastAPI()


class KorniaController:
    def run(self):
        pass


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

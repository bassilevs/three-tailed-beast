from typing import List, Text

from fastapi import FastAPI
from pydantic import BaseModel


class PredictRequest(BaseModel):
    data: Text


class PredictResponse(BaseModel):
    data: Text


app = FastAPI()


@app.post("/predict", response_model=PredictResponse)
def predict(input: PredictRequest):
    return PredictResponse(data=input.data + " right ?")

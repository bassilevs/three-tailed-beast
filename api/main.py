from fastapi import FastAPI, Depends
from pydantic import BaseModel

from .story_time.gpt_2_pytorch import Model, get_model


class PredictRequest(BaseModel):
    data: str


class PredictResponse(BaseModel):
    data: str


app = FastAPI()


@app.get("/ping")
def ping():
    return "version 2.0"


@app.post("/predict", response_model=PredictResponse)
def predict(x: PredictRequest, model: Model = Depends(get_model)):
    x = x.data
    y_pred = model.get_next_n_words(x, 3)
    result = PredictResponse(data=y_pred)

    return result

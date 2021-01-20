from fastapi import FastAPI, Depends
from pydantic import BaseModel, validator

from .alexaDL.model import Model, get_model, n_features
from typing import List


class PredictRequest(BaseModel):
    data: List[str]

    @validator("data")
    def check_dimensionality(cls, words):
        if len(words) != n_features:
            raise ValueError(f"Input must contain {n_features} words")

        return words


class PredictResponse(BaseModel):
    data: str


app = FastAPI()


@app.post("/predict", response_model=PredictResponse)
def predict(x: PredictRequest, model: Model = Depends(get_model)):
    x = x.data
    y_pred = model.predict(x)
    result = PredictResponse(data=y_pred)

    return result

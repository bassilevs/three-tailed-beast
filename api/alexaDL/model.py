import joblib
import numpy as np
from pathlib import Path


class Model:
    def __init__(self, model_path: str = None):
        self._model = None
        self._model_path = model_path
        # self.load()

    def train(self, X: np.ndarray, y: np.ndarray):
        pass

    def predict(self, X):
        return 'prediction'

    def save(self):
        if self._model is not None:
            joblib.dump(self._model, self._model_path)
        else:
            raise TypeError("The model is not trained yet, use .train() before saving")

    def load(self):
        try:
            self._model = joblib.load(self._model_path)
        except:
            self._model = None
        return self


model_path = Path(__file__).parent / "model.joblib"
n_features = 3
model = Model(model_path)


def get_model():
    return model


if __name__ == "__main__":
    # X, y = load_data(return_X_y=True)
    # model.train(X, y)
    # model.save()
    pass

from app.configs import nlu_model
from app.dtos.inputs import PredictionForm
from banking_nlu.utils.schemas  import ModelPrediction


def predict(form:PredictionForm) -> ModelPrediction:
    prediction = nlu_model.banking_nlu.predict(form.text)
    return prediction
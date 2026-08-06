from fastapi import APIRouter

from app.dtos.inputs import PredictionForm
from app.services import prediction_service


router = APIRouter(prefix="/predictions")

@router.post("/")
def predict(form:PredictionForm):
    return prediction_service.predict(form)
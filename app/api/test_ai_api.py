from fastapi import APIRouter

from app.dtos.inputs import PredictionForm


router = APIRouter(prefix="/test-ai")

@router.post("/")
def test_ai(form:PredictionForm):
    return {
        "text": form.text,
        "intents": [
            {
                "label": "transfer_fund",
                "confidence": 100,
                "entities": [
                    {
                        "label": "receiver",
                        "value": "Aung Aung",
                    },
                    {
                        "label": "amount",
                        "value": "20000",
                    }
                ]
            }
        ]
    }
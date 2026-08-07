from fastapi import APIRouter


router = APIRouter(prefix="/test-ai")

@router.post("/")
def test_ai():
    return "Prediction: Works"
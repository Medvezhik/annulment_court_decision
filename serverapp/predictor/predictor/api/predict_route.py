from fastapi import APIRouter

from predictor.schemas.predict import PredictSchema
import predictor.ml_model as ml_model

predict_router = APIRouter()


@predict_router.get("/predict", response_model=PredictSchema)
def predict(text: str):
    predict = ml_model.predict(text)
    return PredictSchema(predict=predict)

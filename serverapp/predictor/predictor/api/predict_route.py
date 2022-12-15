from fastapi import APIRouter

from predictor.schemas.predict import PredictSchema, PredictInputSchema
import predictor.ml_model as ml_model

predict_router = APIRouter()


@predict_router.get("/predict", response_model=PredictSchema)
def predict(input_schema: PredictInputSchema):
    predict = ml_model.predict(input_schema.text)
    return PredictSchema(predict=predict)

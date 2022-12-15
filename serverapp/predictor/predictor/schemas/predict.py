from pydantic import BaseModel


class PredictSchema(BaseModel):
    predict: float

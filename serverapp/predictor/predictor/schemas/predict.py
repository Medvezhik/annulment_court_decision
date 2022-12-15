from pydantic import BaseModel


class PredictInputSchema(BaseModel):
    text: str


class PredictSchema(BaseModel):
    predict: float

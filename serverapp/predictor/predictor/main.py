import uvicorn
from fastapi import FastAPI

from predictor.api.predict_route import predict_router
from predictor.config import Config

cfg = Config()

app = FastAPI()
app.include_router(predict_router)


if __name__ == "__main__":
    uvicorn.run(
        "predictor.main:app", host="0.0.0.0", port=cfg.port, reload=False, debug=False
    )

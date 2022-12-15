import os


class Config:
    vectorizer_path: str = os.environ["VECTORIZER_PATH"]
    model_path: str = os.environ["MODEL_PATH"]
    port: int = os.getenv("SERVER_PORT", 8080)

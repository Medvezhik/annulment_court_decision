import os


class Config:
    vectorizer_path: str = os.environ["VECTORIZER_PATH"]
    model_path: str = os.environ["MODEL_PATH"]
    port: int = int(os.getenv("SERVER_PORT", 8080))
    # Disable model and give a const value as a predict.
    # Only for debugging purposes
    disable_model: bool = bool(int(os.getenv("DISABLE_MODEL", 0)))

from dataclasses import dataclass
from typing import List

from yaml import load, Loader


@dataclass
class Config:
    # Telegram API Token to access Telegram Bot API
    tg_api_token: str
    # Words to search inside the document to determine if it is
    # court decision or not:
    court_required_words: List[str]
    # Directory to store documents, loaded from telegram for parsing
    ms_docs_dir: str = "ms_docs"
    # Max supported file size in bytes.
    # All the files exceeding it will be ignored
    max_file_size: int = 1000000


def load_cfg(path="config.yml") -> Config:
    with open(path, "r") as f:
        cfg = load(f, Loader)
    return Config(**cfg)

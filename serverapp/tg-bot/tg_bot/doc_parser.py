import os.path
from typing import List

import docx
import requests
from docx.opc.exceptions import OpcError

from tg_bot.config import Config
from tg_bot.exceptions import BotException, UnsupportedFileTypeException


def is_tg_file_court_decision(file_id, bot, cfg: Config):
    file_info = bot.get_file(file_id)
    _, ext = os.path.splitext(file_info.file_path)
    if ext.lower() not in [".doc", ".docx"]:
        raise BotException(f"Unsupported file format: {ext}!")

    try:
        response = requests.get(
            f"https://api.telegram.org/file/bot{cfg.tg_api_token}/{file_info.file_path}",
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        print(
            f"Failed to retrieve information about the file at path '{file_info.file_path}': {e}"
        )
        raise BotException("Failed to retrieve information about the file")

    if not os.path.exists(cfg.ms_docs_dir):
        os.makedirs(cfg.ms_docs_dir, exist_ok=True)
    tmp_file = os.path.join(cfg.ms_docs_dir, f"{file_id}{ext}")
    with open(tmp_file, "wb") as f:
        f.write(response.raw.read())

    return is_ms_file_court_decision(tmp_file, cfg.court_required_words)


def get_text_from_tg_file(file_id, bot, cfg: Config) -> str:
    file_info = bot.get_file(file_id)
    _, ext = os.path.splitext(file_info.file_path)
    if ext.lower() not in [".doc", ".docx"]:
        raise UnsupportedFileTypeException()

    try:
        response = requests.get(
            f"https://api.telegram.org/file/bot{cfg.tg_api_token}/{file_info.file_path}",
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        print(
            f"Failed to retrieve information about the file at path '{file_info.file_path}': {e}"
        )
        raise BotException("Failed to retrieve information about the file")

    if not os.path.exists(cfg.ms_docs_dir):
        os.makedirs(cfg.ms_docs_dir, exist_ok=True)
    tmp_file = os.path.join(cfg.ms_docs_dir, f"{file_id}{ext}")
    with open(tmp_file, "wb") as f:
        f.write(response.raw.read())

    try:
        ms_doc = docx.Document(tmp_file)
    except OpcError as e:
        print(f"Failed to parse file {tmp_file} with docx library: {e}")
        raise BotException(f"Failed to parse file {tmp_file}")

    text = " ".join(p.text for p in ms_doc.paragraphs)
    return text


def is_text_court_decision(text: str, key_words: List[str]):
    for w in key_words:
        if w in text:
            print(f"Detected key word '{w}' in text")
            return True
    return False


def is_ms_file_court_decision(path, key_words: List[str]):
    try:
        ms_doc = docx.Document(path)
    except OpcError as e:
        print(f"Failed to parse file {path} with docx library: {e}")
        raise BotException(f"Failed to parse file {path}")

    for p in ms_doc.paragraphs:
        for w in key_words:
            if w in p.text:
                return True
    return False

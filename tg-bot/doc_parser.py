import os.path

import docx
import requests
import telebot

from config import load_cfg
from exceptions import BotException


def is_file_court_decision(bot, file_id):
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
        print(f"Failed to retrieve information about the file at path '{file_info.file_path}': {e}")
        raise BotException(f"Failed to retrieve information about the file")

    if not os.path.exists(cfg.ms_docs_dir):
        os.makedirs(cfg.ms_docs_dir, exist_ok=True)
    tmp_file = os.path.join(cfg.ms_docs_dir, f"{file_id}{ext}")
    with open(tmp_file, "wb") as f:
        f.write(response.raw.read())

    ms_doc = docx.Document(tmp_file)
    for p in ms_doc.paragraphs:
        for w in cfg.court_required_words:
            if w in p.text:
                return True

    return False


file_info = {
    "file_id": "BQACAgIAAxkBAAMaY3naNgfVv0zKd7Q6FWTDYNUJPAEAAmAhAAJ2zNBL4CXB7mJG7RIrBA",
    "file_path": "documents/file_6.doc",
    "file_size": 35223,
}

cfg = load_cfg()
tg_api_token = cfg.tg_api_token
bot = telebot.TeleBot(tg_api_token)

res = is_file_court_decision(bot, file_id=file_info["file_id"])
print(res)
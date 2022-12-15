import telebot
import requests

from tg_bot.config import load_cfg
from tg_bot.doc_parser import (
    is_text_court_decision,
    get_text_from_tg_file,
)
from tg_bot.exceptions import BotException, UnsupportedFileTypeException

cfg = load_cfg()

if cfg.tg_api_token is None or len(cfg.tg_api_token) == 0:
    raise Exception("tg_api_token is not defined!")

bot = telebot.TeleBot(cfg.tg_api_token)


def get_predict(text: str):
    request_url = cfg.predictor_api_url + "/predict"
    response = requests.get(
        request_url,
        json={"text": text},
    )
    if response.status_code != 200:
        raise BotException(
            f"{response.status_code} for url {request_url}: {response.content}"
        )
    p = float(response.json()["predict"])

    p = int(p * 100)
    # Sanity check - restrict possible values to [0; 100]
    # In case predictor returns incorrect value
    p = max(0, min(p, 100))

    return p


@bot.message_handler(commands=["start", "help"])
def start(m, res=False):
    bot.send_message(
        m.chat.id,
        "Привет! Я annulment_court_decision_bot. Пришлите мне решение суда и я оценю "
        "вероятность успешной апелляции.",
    )


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(
        message.chat.id, "Пожалуйста, пришлите решение суда в формате doc/docx"
    )


@bot.message_handler(content_types=["document"])
def handle_docs(message):
    if message.document.mime_type not in [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        bot.send_message(
            message.chat.id, "Пожалуйста, пришлите решение суда в формате doc/docx"
        )
        return

    text = ""
    try:
        # TODO: handle asynchronously
        text = get_text_from_tg_file(message.document.file_id, bot, cfg)
    except UnsupportedFileTypeException as e:
        print(e)
        bot.send_message(
            message.chat.id,
            "Неподдерживаемый формат файла. Поддерживаются только файлы в формате '.doc' и '.docx'",
        )
        return
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Не удалось прочитать файл!")
        return

    if not is_text_court_decision(text, key_words=cfg.court_required_words):
        bot.send_message(
            message.chat.id,
            "Похоже, что присланный документ не является судебным решением.",
        )
        return

    try:
        p = get_predict(text)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Не удалось проанализировать файл!")
        return

    bot.send_message(message.chat.id, f"Вероятность успешной апелляции: {p}%")


print("Starting listening to messages...")
bot.polling(none_stop=True, interval=0)

import os.path

import telebot

from tg_bot.config import load_cfg
from tg_bot.doc_parser import is_file_court_decision
from tg_bot.exceptions import BotException

cfg = load_cfg()

if cfg.tg_api_token is None or len(cfg.tg_api_token) == 0:
    raise Exception("tg_api_token is not defined!")

bot = telebot.TeleBot(cfg.tg_api_token)


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
    if message.document.mime_type not in ["application/msword", 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        bot.send_message(
            message.chat.id, "Пожалуйста, пришлите решение суда в формате doc/docx"
        )
        return

    # TODO: handle asynchronously
    file_info = bot.get_file(message.document.file_id)
    _, ext = os.path.splitext(file_info.file_path)
    if ext.lower() not in [".doc", ".docx"]:
        bot.send_message(
            message.chat.id,
            f"Неподдерживаемый формат файла. Поддерживаются только файлы в формате '.doc' и '.docx'",
        )
        return

    try:
        if not is_file_court_decision(message.document.file_id, bot, cfg):
            bot.send_message(
                message.chat.id,
                f"Похоже, что присланный документ не является судебным решением.",
            )
            return
    except BotException:
        bot.send_message(message.chat.id, f"Не удалось прочитать файл.")
        return

    bot.send_message(message.chat.id, "Вероятность успешной апелляции: 100%")


print("Starting listening to messages...")
bot.polling(none_stop=True, interval=0)

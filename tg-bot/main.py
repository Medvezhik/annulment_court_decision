from yaml import load, Loader
import telebot
import docx

court_required_words = [
    "РЕШЕНИЕ",
    "Решение",
    "Р Е Ш Е Н И Е",
    "Именем Российской Федерации",
    "именем Российской Федерации",
    "ИМЕНЕМ РОССИЙСКОЙ ФЕДЕРАЦИИ",
    "УСТАНОВИЛ",
    "У С Т А Н О В И Л",
    "РЕШИЛ",
    "Р Е Ш И Л",
]

with open("config.yml", "r") as f:
    cfg = load(f, Loader)

tg_api_token = cfg["tg_api_token"]
if tg_api_token is None or len(tg_api_token) == 0:
    raise Exception("tg_api_token is not defined!")

bot = telebot.TeleBot(tg_api_token)


@bot.message_handler(commands=["start", "help"])
def start(m, res=False):
    bot.send_message(
        m.chat.id,
        "Привет! Я annulment_court_decision_bot. Пришлите мне решение суда и я оценю "
        "вероятность успешной аппеляции.",
    )


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, "Пожалуйста, пришлите решение суда в формате doc/docx")


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.mime_type != "application/msword":
        bot.send_message(message.chat.id, "Пожалуйста, пришлите решение суда в формате doc/docx")
        return

    bot.send_message(message.chat.id, message.document.mime_type)



bot.polling(none_stop=True, interval=0)

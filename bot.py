import os
import telebot

TOKEN_VAR = "TG_API_TOKEN"
if TOKEN_VAR not in os.environ:
    raise Exception(f"Define {TOKEN_VAR} in your environment!")

# Создаем экземпляр бота
bot = telebot.TeleBot(os.environ[TOKEN_VAR])


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Я на связи. Напиши мне что-нибудь )")


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, "Вы написали: " + message.text)


# Запускаем бота
bot.polling(none_stop=True, interval=0)

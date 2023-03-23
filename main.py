import telebot
from config import money, TOKEN
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help'])
def help(messange: telebot.types.Message):
    text = "Справка по работе с ботом.\n " \
           "Чтобы начать работу введите команду боту в следущем формате:\n" \
           "<имя валюты> <в какую валюту первести> <количество валюты>\n\n" \
           "Пример, чтобы перевесть 5 долларов в рубли, введите:\n" \
           "доллар рубль 5\n\n" \
           "/values - список доступных валют\n" \
           "/start - стартовое приветствие\n" \
           "/help - справка по работе с ботом"
    bot.send_message(messange.chat.id, text)

@bot.message_handler(commands=['start'])
def start(messange: telebot.types.Message):
    text = "Добро пожаловать в бот по конвертации валют.\n" \
           " Справка по работе бота - /help"
    bot.send_message(messange.chat.id, text)

@bot.message_handler(commands=['values'])
def values(messange: telebot.types.Message):
    text = "Доступные валюты:"
    for key in money.keys():
        text = "\n".join((text, key))
    bot.send_message(messange.chat.id, text)

@bot.message_handler(content_types=["text"])
def converter(messange):
    values = messange.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        base, quote, amount = values
        convert = Converter.api(base, quote, amount)
        bot.reply_to(messange, f'{amount} {base} = {convert} {quote}')
    except APIException as e:
        bot.reply_to(messange, f"Ошибка в команде:\n{e}")

bot.polling()

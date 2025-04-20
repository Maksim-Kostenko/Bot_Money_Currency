import os

import telebot
import dotenv

from extensions import Currency

dotenv.load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

#Перечень доступных валют к переводу (изменяем при необходимости)
currency = {
    'Доллар': 'USD',
    'Рубль': 'RUB',
    'Евро': 'EUR',
    'Польский злотый': 'PLN'
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome_and_instruction(message):
    """Ответ на команды /start и /help"""
    text = (f'Добрый день, {message.chat.username}!\n'
            f'Чтобы воспользоваться функциями бота тебе необходимо отправить сообщение в формате <Валюта, цену которой надо узнать>, '
            f'<Валюта , в которой надо узнать цену>, <Количество валюты>\n'
            f'Для того, что бы ознакомиться с доступным перечнем валюты отправьте в чат /value')
    bot.reply_to(message, text)

@bot.message_handler(commands=['value'])
def send_currency_list(message):
    """Ответ на команды /value"""
    text = f'Доступная к конвертации валюта: \n'
    text += ', '.join(currency.keys())
    bot.reply_to(message, text)

#Подумать на сколько рационально использовать , content_types=['text']
@bot.message_handler(func=lambda message: True)
def send_result_currency_transfer(message):
    """Отправка сообщения с результатом перевода валют"""
    base, quote, amount = message.text.split(' ')
    result_transfer = Currency.get_price(currency[base], currency[quote], amount)
    text = f'{result_transfer}\n'
    bot.reply_to(message, text)

try:
    bot.polling(none_stop=True)
except TeleBotException as e:
    logging.error(e)



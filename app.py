import os
import time

from telebot.apihelper import ApiException
import telebot
import dotenv
import logging

from extensions import Convertion, ConvertionException

dotenv.load_dotenv()

#Реализация и настройка logger
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler('bot_errors.log')])

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

#Перечень доступных валют к переводу (изменяем при необходимости)
currency = {
    'Доллар': 'USD',
    'Рубль': 'RUB',
    'Евро': 'EUR',
    'Польский_злотый': 'PLN'
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome_and_instruction(message):
    """Ответ на команды /start и /help"""
    text = (f'Добрый день, {message.chat.username}!\n'
            f'Чтобы воспользоваться функциями бота тебе необходимо отправить сообщение в формате <Валюта, цену которой надо узнать>, '
            f'<Валюта , в которой надо узнать цену>, <Количество валюты>\n'
            f'Для того, что бы ознакомиться с доступным перечнем валюты отправьте в чат /value .')
    bot.reply_to(message, text)

@bot.message_handler(commands=['value'])
def send_currency_list(message):
    """Ответ на команды /value"""
    text = f'Доступная к конвертации валюта: \n'
    text += '\n'.join(currency.keys())
    bot.reply_to(message, text)

#Подумать на сколько рационально использовать , content_types=['text']
@bot.message_handler(func=lambda message: True)
def send_result_currency_transfer(message):
    """Отправка сообщения с результатом перевода валют"""

    try:
        quote_ticker, base_ticker, amount = Convertion.convert(message, currency)
        result_convertion = Convertion.get_price(base_ticker, quote_ticker, amount)
        text = f'{result_convertion}\n'
        bot.reply_to(message, text)
    except ConvertionException as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")



def start_bot():
    while True:
        try:
            logging.info('Старт бота...')
            bot.polling(none_stop=True)
        #Протестировать, на сколько рационально использовать торлько ApiException, мб корректно использовать еще просто Exception?
        except ApiException as e:
            logging.critical(e, exc_info=True)
            logging.info('Перезагрузка бота через 5 секунд...')
            time.sleep(5) #Выдержка, вдруг ошибка самоустранима


if __name__ == '__main__':
    start_bot()
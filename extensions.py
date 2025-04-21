import os

import requests
import dotenv
import json


dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY') #https://currencylayer.com/dashboard

class ConvertionException(Exception):
    pass


class Convertion:

    @staticmethod
    def convert(message, currency):
        base, quote, amount = message.text.split(' ')

        if len(message.text.split()) != 3:
            raise ConvertionException('Направленное количество параметров не соответствует ожидаемому')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(
                'Не удалось определить валюту, проверьте корректность написания и наличие в /value')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(
                'Не удалось определить валюту, проверьте корректность написания и наличие в /value')

        try:
            amount = int(amount)
        except ValueError:
            raise ConvertionException('Число должно быть представлено в виде арабских цифр')

        if amount <= 0:
            raise ConvertionException('Число не может быть меньше или равно 0')

        return quote_ticker, base_ticker, amount


    @classmethod
    def get_price(cls, base: str, quote: str, amount: str):
        req = requests.get(f'http://apilayer.net/api/live?access_key={API_KEY}&currencies={quote}&source={base}&format=1')
        a = json.loads(req.text)
        price = float(a['quotes'][f'{base}{quote}'])
        return price * int(amount)
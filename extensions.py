import os

import requests
import dotenv
import json

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY') #https://currencylayer.com/dashboard

class APIException(Exception):
    """Класс для базовых ошибок API"""
    pass


class Convertion:
    """Основной класс, где реализовано получение данных от пользователя и API и конвертация"""

    @staticmethod
    def convert(message, currency):
        """Обработка полученных данных из сообщения пользователя, замена введенных данных от пользователя на данные из таблицы currency"""
        if len(message.text.split(' ')) != 3:
            raise APIException('Не верный формат. Используйте: <Валюта, цену которой надо узнать>, '
            f'<Валюта , в которой надо узнать цену>, <Количество валюты>')

        base, quote, amount = message.text.split(' ')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена, проверьте корректность написания и наличие в /value')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена, проверьте корректность написания и наличие в /value')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException('Число должно быть представлено в виде арабских цифр')

        if amount <= 0:
            raise APIException('Число не может быть меньше или равно 0')

        return quote_ticker, base_ticker, amount


    @classmethod
    def get_price(cls, base: str, quote: str, amount: str):
        """Получение данных от API currencylayer, конвертация"""
        try:
            response = requests.get(f'http://apilayer.net/api/live?access_key={API_KEY}&currencies={quote}&source={base}&format=1')
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise APIException("Таймаут при подключении к серверу валют")
        except requests.exceptions.ConnectionError:
            raise APIException("Ошибка подключения к серверу валют")
        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка сети: {str(e)}")
        data = json.loads(response.text)
        price = float(data['quotes'][f'{base}{quote}'])
        return price * int(amount)
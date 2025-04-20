import os

import requests
import dotenv
import json


dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY') #https://currencylayer.com/dashboard

class Currency:

    @classmethod
    def get_price(cls, base: str, quote: str, amount: str):
        req = requests.get(f'http://apilayer.net/api/live?access_key={API_KEY}&currencies={quote}&source={base}&format=1')
        a = json.loads(req.text)
        price = float(a['quotes'][f'{base}{quote}'])
        return price * int(amount)

# class CurrencyException(ApiException):
#     pass
import requests
import json


class ConvertionException(Exception):
    pass

# получение информации о запрашиваемой пользователем валюте и некоторые проверки
class CurrencyExchanger:
    @staticmethod
    def exchange(quote: str, amount: float):
        r = requests.get(f'https://www.nbrb.by/api/exrates/rates/{quote}?parammode=2')
        total_base = json.loads(r.content)

        if len(quote) != 3:
            raise ConvertionException('Неверная валюта.')

        try:
            amount = float(amount)
        except:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        if Exception == 'Expecting value':
            raise ConvertionException('шляпа')
        return total_base

# получение списка доступных валют
class AvailableCurrencies:
    @staticmethod
    def currencies():
        r = requests.get(f'https://www.nbrb.by/api/exrates/rates?periodicity=0')
        available_base = json.loads(r.content)
        return available_base
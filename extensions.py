import requests
import json
from config import money

class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def api(base, quote, amount):
        try:
            base_key = money[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")
        try:
            quote_key = money[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")
        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_key}&from={base_key}&amount={amount}"
        payload = {}
        headers = {"apikey": "Fbny0o73H57P1zvb66wRirGFCN9CFYeH"}
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.content)
        convert = (round(resp['result'], 2))
        return convert


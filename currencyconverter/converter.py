import requests
from decimal import Decimal

class ConverterError(Exception):
    pass
class ConvertationError(ConverterError):
    pass


class CurrencyConverter:
    # E.g https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT
    BINANCE_TICKER_PRICE_ENDPOINT = 'https://api.binance.com/api/v1/ticker/price?symbol='
    
    def __init__(self, data):
        for key in data:
            setattr(self, key, data[key])
        # If amount is not specified, it will be equal to 1
        self.in_amount = int(self.in_amount) if hasattr(self, 'in_amount') else 1 

        self.rate = self._fetch_binance_ticker_price()
        # print(self.rate)

    # Fetches price rate from Binance API
    def _fetch_binance_ticker_price(self):
        try:
            binance_result_json = requests.get(
                f'{CurrencyConverter.BINANCE_TICKER_PRICE_ENDPOINT}{self.in_currency}{self.out_currency}').json()
            price = binance_result_json['price']
            print(price)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        except Exception as err:
            raise ConvertationError(f'Oops {err}: {binance_result_json}')

        return price

    def __str__(self):
        return f'{self.in_amount}{self.in_currency}{self.out_currency}'

    # Get price rates: Decimal(default) or Integer
    def get_rate(self):
        return Decimal(self.rate)
    def get_int_rate(self):
        return int(Decimal(self.rate))

    # Convert methods: Decimal(default), or Integer
    def convert(self):
        return self.in_amount * self.get_rate()
    def int_convert(self):
        return self.in_amount * self.get_int_rate()


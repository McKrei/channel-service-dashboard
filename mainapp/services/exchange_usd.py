import requests
from datetime import datetime


class USD():
    '''
    Через класс получаем актуальную цену на USD через метод get_price.
    остальные методы и аргументы скрыты.
    '''
    _price = None
    _date = None

    def _get_exchange_usd_and_update(self, today: str):
        '''Получаем текущую дату. Запрос курса на сегодня. Обновляем цену и дату.'''
        resp = requests.get(
            'https://www.cbr-xml-daily.ru/daily_json.js').json()
        self._price = float(resp['Valute']['USD']['Value'])
        self._date = today

    @property
    def get_price(self) -> float:
        '''
        Метод для получения цены USD на сегодня.
        Если данные есть возвращаем, если нет обновляем и возвращаем
        '''
        today = str(datetime.today())[:10]
        if self._price and self._date == today:
            return self._price
        self._get_exchange_usd_and_update(today)
        return self._price

import time
from datetime import datetime, date

from django.core.management.base import BaseCommand
from django.conf import settings
from .telegram import telegram_report

from mainapp.models import Order
from config.conf import sec_sleep, hour_telegram_report


class Command(BaseCommand):
    '''
    В команде проверяем каждые conf.sec_sleep секунд наличе обновлений в гугл таблице,
    сохраняем их в БД. Отправляем в заданное время отчет в телеграм о просроченных заказах
    '''
    help = f'Обновление БД каждые {sec_sleep}сек'

    def handle(self, *args, **kwargs):
        try:
            while True:
                Order.update_data()
                if datetime.now().hour == hour_telegram_report:
                    orders = Order.get_delay_orders()
                    if len(orders):
                        telegram_report(orders)
                Order.report_orders()
                time.sleep(sec_sleep)
        except KeyboardInterrupt:
            print('Завершил работу')

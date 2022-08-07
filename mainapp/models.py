import datetime

from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.conf import settings


class Order(models.Model):
    '''
    Храним информацию о заказах, вся работа с БД через методы модели
    '''
    id = models.IntegerField(primary_key=True)
    number_order = models.CharField(max_length=256, blank=True)
    price_usd = models.FloatField(blank=True)
    delivery_date = models.DateField(blank=True)
    price_rub = models.FloatField(blank=True)

    def _normalize_data(data: list[list]) -> list[tuple]:
        '''Преобразование сырых данных из Sheets к необходимому формату'''
        usd = settings.USD.get_price
        result = []
        for order_line in data:
            try:
                num, order, price, date = order_line
                num = int(num)
                if price:
                    price = float(price.replace(',', '.'))
                    price_rub = round(price * usd, 2)
                else:
                    price, price_rub = 0, 0

                day, month, year = map(int, date.split('.'))
                date = datetime.date(year=year, month=month, day=day)
                result.append((num, order, price, date, price_rub))
            except ValueError:
                print('Данну строку не получилось добавить\n', order_line)
                continue
        return result

    def _request_db(date: tuple[tuple]) -> None:
        '''Получаем данные которые отличаются от данных в БД и обновляем либо создаем объект'''
        for id, order_num, price, date, price_rub in date:
            order, update = Order.objects.update_or_create(id=id, defaults={
                'number_order': order_num,
                'price_usd': price,
                'delivery_date': date,
                'price_rub': price_rub
            })
            order.save()

    def update_data() -> None:
        '''
        Обновляем данные в БД.
        Получаем данные с гугл, преобразуем данные, сравниваем с тем, что уже есть.
        Если есть отличия вносим изменяи
        '''
        original_data = settings.TABLE.get_data
        normal_data = Order._normalize_data(original_data)
        order = Order.objects.all().values_list(
            'id', 'number_order', 'price_usd', 'delivery_date', 'price_rub')
        data_for_write = tuple(set(normal_data) - set(order))
        print(f'Отличается {len(data_for_write)} строк')
        Order._request_db(data_for_write)

    def get_delay_orders() -> list[tuple]:
        '''
        Получаем все заказы, у которых дата < today.
        Возвращаем поля: 'number_order', 'price_usd', 'delivery_date'
        которые необходимы для отчета в телеграм
        '''
        orders = Order.objects.exclude(delivery_date__gte=datetime.date.today()
                                       ).values_list('number_order', 'price_usd', 'delivery_date')
        return orders

    def report_orders():
        '''
        Возвращаем данные необходимые для дашборда:
        orders - все объекты из базы данных
        sum_price - Итоговая стоимость всех заказов в долларах
        count_delay - Количество заказов с просрочкой
        days - Дни для вывода на графике
        sums - Суммы за день для вывода на графике
        '''
        orders = Order.objects.all()
        sum_price = int(orders.aggregate(Sum('price_usd'))['price_usd__sum'])
        count_delay = orders.exclude(
            delivery_date__gte=datetime.date.today()).count()
        result = orders.order_by('delivery_date').annotate(day=TruncDay('delivery_date')
                                                           ).values('day').annotate(sum=Sum('price_usd')).values('day', 'sum')
        indent_between_date = 3  # Что бы все влезло будем выводить каждую n-ю дату
        days = []
        sums = []
        for i, order_dict in enumerate(result):
            if not i % indent_between_date:
                days.append(str(order_dict['day']))
            else:
                days.append('')
            sums.append(order_dict['sum'])

        return orders, sum_price, count_delay, days, sums

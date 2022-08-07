import operator

from django.shortcuts import render
from django.conf import settings

from mainapp.models import Order


def index(request):
    '''
    Получаем необходимые данные для дашборда и передаем их в template
    '''
    orders, sum_price, count_delay, days, sums = Order.report_orders()
    content = {
        'title': 'Test Task',
        'orders': sorted(orders, key=operator.attrgetter('id')),
        'sum_price': sum_price,
        'count_delay': count_delay,
        'count_orders': orders.count(),
        'days': days,
        'sums': sums,
    }

    return render(request, 'mainapp/index.html', content)

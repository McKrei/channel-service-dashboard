import telebot
from telegram import ParseMode
from prettytable import PrettyTable

from config.conf import TELEGRAM_USER_ID, hour_telegram_report, TOKEN

bot = telebot.TeleBot(TOKEN)


def create_mes(data: list[tuple]) -> str:
    '''Получаем  данне по просроченным ордерам и формируем отчет'''
    start_mes = f'{len(data)} Просроченных ордеров\n'
    table = PrettyTable()
    table.field_names = ['Ордер', 'Цена', 'Дата']
    for order, price, date in data:
        table.add_row((order, price, date))
    return f'{start_mes}<pre>{table}</pre>'


def telegram_report(data: list[tuple]) -> None:
    '''Получаем данне по просроченным ордерам и отправляем отчет на user_id из conf'''
    mes = create_mes(data)
    bot.send_message(TELEGRAM_USER_ID, mes, parse_mode=ParseMode.HTML)

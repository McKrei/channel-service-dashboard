# Id пользователя в телеграмм которому будем отправлять информацию
TOKEN = 'Твой токе от телеграм бота'
TELEGRAM_USER_ID = 'Твой user_id в телеграмм'
hour_telegram_report = 9 # В какое время будет приходить отчет по просроченным заказам 9 -это 9:00 утра
sec_sleep = 60 # Как часто будем обновлять данные из гугл таблицы

# Настройки Гугл таблиц
SAMPLE_SPREADSHEET_ID = '1KMc0fb4LBNphJNqmnObRgsIxUOTiA3zQC1AqBcP_5OM' # id таблицы
SAMPLE_RANGE_NAME = 'Лист1!A2:D1000' # лист на котором находится таблица и диапазон таблицы


'''Django'''
DJANGO_SECRET_KEY = '' # "django-insecure-j^0vme4%8j-5@=9cx2k&70q4q#t)6+b)d^+5i@_jr@(%ks2+xa"

#postgresql
NAME = 'имя базы данных'
USER = 'имя пользователя postgresql'
PASSWORD = 'твой пароль от postgresql'
DB_HOST = 'localhost'
PORT = 5432

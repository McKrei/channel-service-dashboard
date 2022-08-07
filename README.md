## Для запуска необходимо:
1. Клонировать репозиторий
2. Заполни файл config/conf.py
3. Создать виртуальное окружение и установить зависимости:
    * pip install -r requirements.txt
4. Установить миграции для БД
    * Возможно запросит доступ к google
5. Запустить команду которая будет обновлять базу данных
    * python manage.py start_update
    * ! При первом запуске, создаст токен, нужно будет подтвердить доступ к гугл аккаунту.
    * Доступ к моему приложению google api  предоставлен только аккаунту проверяющего. Для запуска в остальных случаях нужно создать приложение по инструкции: https://developers.google.com/workspace/guides/create-project
    После создания json файл назовите "credentials.json" и переместите в папку config
6. После того как команда запущенна и база данных обновляется. Запуск локального сервера:
    * python manage.py runserver
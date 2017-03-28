# hselingprojects
Проекты Школы Лингвистики

Это код для сайта "Проекты Школы Лингвистики".

## Зависимости
* Python 3
* Django 1.10
* django-password-reset
* django-cleanup

## Как запустить
Чтобы сайт заработал в корне проекта должен быть файл `.secret.json` с таким содержанием:

```
{
  "SECRET_KEY": "здесь ваш секретный ключ",
  "EMAIL_HOST_USER": "адрес почты, с которой будут отправляться уведомления пользователям",
  "EMAIL_HOST_PASSWORD": "пароль",
  "DEFAULT_FROM_EMAIL": "снова адрес почты",
  "DEBUG": true
}
```

Нужен гугловский почтовый аккаунт , так как мы используем почтовый сервер `gmail`. 
Кроме того, в этом аккаунте должна быть отключена двухфакторная аутентификация и 
разрешен [доступ](https://support.google.com/accounts/answer/6010255?hl=ru) ненадежным приложениям.

Когда это сделано, нужно в терминале перейти в корень проекта и запустить:

* Если у вас еще нет базы данных с проектами:
    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```
* Если у вас есть база данных:
    ```
    python manage.py runserver
    ```

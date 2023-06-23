# This project is built as an example for project with posts(including photos and authorization) based on Django #

## In order to start using it there are some instructions:
1. Download all the requirements 
2. Put all your needed info in settings(such as Secret_key and email from which you gonna send emails)
```
SECRET_KEY = '##'

```
```
DEFAULT_FROM_EMAIL = "###" #your full email

EMAIL_HOST = 'smtp.yandex.ru'  # server adress of Yandex is the same for everyone
EMAIL_PORT = 465  # port smtp is also the same
EMAIL_HOST_USER = '###'  # username, if your email is user@gmail.com just write everything from it before @
EMAIL_HOST_PASSWORD = '###'  # password from email
EMAIL_USE_SSL = True
```

3. In terminal run:
    * python manage.py makemigrations
    * python manage.py migrate
    * python manage.py createsuperuser(in order to have access to admin 
    panel)
    * python manage.py runserver 


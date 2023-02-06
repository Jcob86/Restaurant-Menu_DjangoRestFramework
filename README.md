# Restaurant Menu API builded in Django Rest Framework

## Project setup

If you are using Windows, you have to use WSL. If Linux/MacOS everything should be fine.

```bash
git clone https://github.com/Jcob86/Restaurant-Menu_DjangoRestFramework.git
cd Restaurant-Menu_DjangoRestFramework
python3 -m venv venv 
source venv/bin/activate
```

You have to setup your database and password in settings.py, then:
```bash
python manage.py migrate
python manage.py createsuperuser ... [optionally to have all permissions]
...
python manage.py runserver
```

## You can find whole API Documentation under this link <a href="http://localhost:8000/swagger/schema" target="_blank">Restaurant API Docs</a>

## Authorization
I highly recommend to use Postman or <a href="https://chrome.google.com/webstore/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj" target="_blank">ModHeader</a> to save your JWT to pass authorization easily


## Message Broker installation
```bash
sudo apt update
sudo apt install redis
redis-server
```

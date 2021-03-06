# DASHBOARD HEADHUNTER
Небольшое приложение для построения графиков по данным с сайта hh.ru доступно по [ссылке](http://learn-python-hh-dashboard.tk).

Данное readme включает в себя инструкцию по быстрому запуску приложения.    
Вопросы сбора данных по расписанию (такая возможность реализована) и запуск flask-приложения не вкючены в данную инструкцию. 

Сервер запущен при помощи сервиса DigitalOcean. Дистрибутив - Ubuntu 20.
В качестве WSGI-сервера использован Gunicorn, web-сервер - Nginx. Сертификат безопасности от Let's Encrypt.

## Приложение состоит из:
* Базы данных в которой храняться данные с hh.ru
* Модулей api_client и db_worker, которые позволяют получать данные с hh.ru и писать их в базу
* flask-приложения для отображения графиков

## Использованные библиотеки:
* SQLAlchemy и Flask-SQLAlchemy - для взаимодействия с СУБД
* requests - для запросов к веб-ресурсам (api)
* Flask - для реализации веб-приложения
* celery[redis] - для запуска сбора данных по рассписанию
* и [многие другие](https://github.com/Jabloco/dashboard_headhunter/blob/main/requirements.txt)

## Для запуска необходимо:
:white_check_mark: Собственно сам Python    
:white_check_mark: Redis (при деплое)    
:white_check_mark: SQLite    
:white_check_mark: Все зависимости из requirements.txt    

## Как запустить:
1. Ставим Python, Redis (при деплое), SQLite
2. Заходим в консоль. Клонируем данный репозиторий.    
3. Переходим в папку приложения.    
    * если используете venv создайте и запустите окружение
    
    cmd
    ```
    python -m venv env
    env\Scripts\activate
    ```
    bash
    ```
    python3 -m venv env
    source env/bin/activate
    ```
4. Устанавливаем зависимости.

cmd\bash
```
pip install -r requirements.txt
```
5. Укажем flask-у из какого файла импортировать проект

cmd
```
set FLASK_APP=dashboard_hh.py
```
bash
```
export FLASK_APP=dashboard_hh.py
```

6. Запускаем flask db upgrade. У нас появится пустая база.

cmd\bash
```
flask db upgrade
```
7. Не выходя из папки запускаем db_worker.py

cmd
```cmd
python db_worker.py
```
bash
```bash
python3 db_worker.py
```
Можно пойти погулять, посмотреть кино или заняться домашними делами.    
Первый сбор данных занимает более часа времени. Связано это в первую очередь с ограничениями, которые накладывает api hh.ru, примерно 7 req\sec\ip.    
Что бы не попасть в бан от api число запросов сокращено до 3 в секунду.    
8. Если совсем не в терпеж, а посмотреть на графики хочется работу воркера можно прервать с помощью Ctrl + C в консоли    
8. Для запуска веб части делаем  
cmd/bash
```
flask run
```  

9. В адресной строке браузера вводим [127.0.0.1:5000](http://127.0.0.1:5000), выбираем любой график и ЛЮБУЕМСЯ :smile:

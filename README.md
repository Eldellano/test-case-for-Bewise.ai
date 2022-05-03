## Тестовое задание для Bewise.ai

![https://img.shields.io/badge/Python-3.8.5-blue](https://img.shields.io/badge/Python-3.8.5-blue)
![https://img.shields.io/badge/SQLAlchemy-1.4.36-red](https://img.shields.io/badge/SQLAlchemy-1.4.36-red)

---
1. С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL).


2. Реализовать на Python3 простой веб сервис (с помощью FastAPI или Flask, например), выполняющий следующие функции:
В сервисе должно быть реализовано REST API, принимающее на вход POST запросы с содержимым вида {"questions_num": integer} ;
---
Запуск в docker: 
```
docker-compose up
```
После сборки сервис будет доступен по адресу - http://127.0.01:5000/ 

---
Сервис имеет один эндпоинт -
* `/questions_num/num`, где num - количество запросов к API jservice.io. Пример - `http://127.0.0.1:5000/questions_num/1`

После выполнения запросов к API, сервис возвращает предыдущую сохраненную запись из БД
Так же, в сервисе реализована проверка наличия в БД полученной записи от API. При наличии такой записи будет совершен новый запрос.

---
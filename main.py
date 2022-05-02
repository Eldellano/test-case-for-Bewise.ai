from fastapi import FastAPI
import uvicorn
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from typing import NoReturn

app = FastAPI()

DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'user_pg',
    'password': '123qwerty',
    'database': 'questions'
}

engine = create_engine(URL(**DATABASE))
DeclarativeBase = declarative_base()


class Answer(DeclarativeBase):
    """Описание таблицы для хранения результатов запросов"""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    id_from_api = Column('id_from_api', Integer)
    question = Column('question', String)
    answer = Column('answer', String)
    created_at = Column('created_at', DateTime)

    def __repr__(self):
        return "".format(self.code)


# Метод create_all создает таблицы в БД, определенные с помощью DeclarativeBase
DeclarativeBase.metadata.create_all(engine)
# Создаем фабрику для создания экземпляров Session.
# Для создания фабрики в аргументе bind передаем объект engine
Session = sessionmaker(bind=engine)
# Создаем объект сессии из вышесозданной фабрики Session
session = Session()


def add_to_db(id_from_api, question, answer, created_at) -> NoReturn:
    """Добавляем новую запись в БД"""
    # подготавливаем запись
    to_db = Answer(id_from_api=id_from_api, question=question, answer=answer, created_at=created_at)
    # Добавляем запись
    session.add(to_db)
    session.commit()


def check_id_in_db(id_from_api: int) -> bool:
    """Проверяем наличие полученной записи в БД"""
    id_in_db = session.query(Answer).filter_by(id_from_api=id_from_api).first()
    if id_in_db is None:
        return True
    else:
        return False


def get_last_record(num: int) -> (object, dict):
    """Получаем последнюю запись из бд"""
    try:
        return session.query(Answer).order_by(desc('id'))[num]
    except IndexError:
        return {}


@app.get('/questions_num/{num}')
def get_item(num: int) -> (object, dict):
    resp = requests.get(f'https://jservice.io/api/random?count={num}')

    for i in resp.json():
        id_from_api = i['id']
        question = i['question']
        answer = i['answer']
        created_at = i['created_at']

        if check_id_in_db(id_from_api):  # Проверка наличия вопроса с таким id в БД
            add_to_db(id_from_api, question, answer, created_at)
        else:
            # Если вопрос с таким id уже есть в БД
            get_item(1)
    return get_last_record(num)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")

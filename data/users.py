import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True) # создание таблицы, поле id
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True) # фамилия
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True) # имя
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # возраст
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True) # Город
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True) # почта
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True) # пароль
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now) # дата создания аккаунта

    journey = orm.relationship("Journey", back_populates='user') # связь со второй таблицей

    def __repr__(self):
        return f'<User> {self.id} {self.surname} {self.name}' # вывод

    def set_password(self, password): # создание пароля
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password): # проверка пароля
        return check_password_hash(self.hashed_password, password)

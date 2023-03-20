import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Journey(SqlAlchemyBase):
    __tablename__ = 'journey'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    month = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    transport = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")) # администратор?
    user = orm.relationship('User')

    def __repr__(self):
        return f'<Journey> {self.country}'

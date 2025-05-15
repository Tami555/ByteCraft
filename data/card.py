import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Card(SqlAlchemyBase):
    __tablename__ = 'Bonus_Cards'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    CardNumber = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Balance = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    Period = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Code = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user = orm.relationship('User', back_populates='card')
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Seller(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Seller'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    FirstName = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    LastName = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='-')
    Email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    PhoneNumber = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Balance = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    
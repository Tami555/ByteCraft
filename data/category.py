import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Category_Products"
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Background = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
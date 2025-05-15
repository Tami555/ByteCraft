import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Reviews(SqlAlchemyBase):
    __tablename__ = 'Reviews'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    UserId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Users.Id'))
    ProductId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Product.Id'))
    Mark = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Data = sqlalchemy.Column(sqlalchemy.Date, nullable=True)

    user = orm.relationship('User')
    product = orm.relationship('Product')


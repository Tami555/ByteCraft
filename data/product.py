import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Product"
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    TechnicalSpecifications = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    QuantityStock = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    IdCategory = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Category_Products.Id'))
    IdSeller = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Seller.Id'))
    category = orm.relationship('Category')
    seller = orm.relationship('Seller')
    reviews = orm.relationship('Reviews')
    like = False

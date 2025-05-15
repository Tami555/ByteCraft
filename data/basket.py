import sqlalchemy
from data.db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Basket(SqlAlchemyBase):
    __tablename__ = 'Basket'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    IdUser = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Users.Id'))
    products = orm.relationship("Product", secondary="Product_Basket")
    user = orm.relationship("User")

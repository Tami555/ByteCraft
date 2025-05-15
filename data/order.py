import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = "Order"
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    IdUser = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Users.Id'))
    Summa = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Data = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    DateReceipt = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    DeliveryAddress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    IdPickUpPoint = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Pick_Up_Point.Id'))
    ShippingMethod = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Type_Delivery.Id'))

    pickup = orm.relationship('PickUpPoint')
    user = orm.relationship('User')
    delivery = orm.relationship('TypeDelivery')
    products = orm.relationship("Product", secondary="Ordered_Goods")
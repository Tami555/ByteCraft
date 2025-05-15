import sqlalchemy
from data.db_session import SqlAlchemyBase


Ordered_Goods = sqlalchemy.Table(
    'Ordered_Goods',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('IdProduct', sqlalchemy.Integer, sqlalchemy.ForeignKey('Product.Id')),
    sqlalchemy.Column('IdOrder', sqlalchemy.Integer, sqlalchemy.ForeignKey('Order.Id')),
    sqlalchemy.Column('Quantity', sqlalchemy.Integer, default=1) 
)
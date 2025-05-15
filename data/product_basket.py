import sqlalchemy
from data.db_session import SqlAlchemyBase


Product_Basket = sqlalchemy.Table(
    'Product_Basket',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('IdProduct', sqlalchemy.Integer, sqlalchemy.ForeignKey('Product.Id')),
    sqlalchemy.Column('IdBasket', sqlalchemy.Integer, sqlalchemy.ForeignKey('Basket.Id')),
    sqlalchemy.Column('Quantity', sqlalchemy.Integer, default=1) 
)

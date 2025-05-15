import sqlalchemy
from data.db_session import SqlAlchemyBase


Favorites = sqlalchemy.Table(
    'Favorites',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('IdProduct', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('Product.Id')),
    sqlalchemy.Column('IdUser', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('Users.Id'))
)
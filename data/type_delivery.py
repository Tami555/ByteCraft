import sqlalchemy
from data.db_session import SqlAlchemyBase

class TypeDelivery (SqlAlchemyBase):
    __tablename__ = 'Type_Delivery'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
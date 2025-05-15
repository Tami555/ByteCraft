import sqlalchemy
from data.db_session import SqlAlchemyBase

class Cites (SqlAlchemyBase):
    __tablename__ = 'Cites'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
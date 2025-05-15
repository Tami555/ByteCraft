import sqlalchemy
from data.db_session import SqlAlchemyBase
import sqlalchemy.orm as orm

class PickUpPoint (SqlAlchemyBase):
    __tablename__ = 'Pick_Up_Point'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    IdCity = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Cites.Id'), default=0)
    cite = orm.relationship("Cites")